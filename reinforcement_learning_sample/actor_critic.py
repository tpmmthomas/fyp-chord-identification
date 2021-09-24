import gym
import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.layers import Add, Multiply
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.backend as K
import tensorflow as tf
import pandas as pd
from env import CryptoSingleEnv
import random
from collections import deque
import time

# OR SIMPLY USE basemark
# determines how to assign values to each state, i.e. takes the state
# and action (two-input model) and determines the corresponding value
class ActorCritic:
    def __init__(self, env):
        self.env = env

        self.learning_rate = 0.001
        self.epsilon = 1.0  # explore or exploit probability
        self.epsilon_decay = 0.9999  # gradually lean towards exploitation
        self.gamma = 0.95  # Future rewards discount rate
        self.tau = 0.125  # Prob of updating the target model

        # ===================================================================== #
        #                               Actor Model                             #
        # Chain rule: find the gradient of chaging the actor network params in  #
        # getting closest to the final value network predictions, i.e. de/dA    #
        # Calculate de/dA as = de/dC * dC/dA, where e is error, C critic, A act #
        # ===================================================================== #

        self.memory = deque(maxlen=2000)
        self.actor_state_input, self.actor_model = self.create_actor_model()
        _, self.target_actor_model = self.create_actor_model()

        # self.actor_critic_grad = tf.placeholder(
        #     tf.float32, [None, self.env.action_space.shape[0]]
        # )  # where we will feed de/dC (from critic)

        # actor_model_weights = self.actor_model.trainable_weights
        # self.actor_grads = tf.gradients(
        #     self.actor_model.output, actor_model_weights, -self.actor_critic_grad
        # )  # dC/dA (from actor)
        # grads = zip(self.actor_grads, actor_model_weights)
        # self.optimize = tf.train.AdamOptimizer(self.learning_rate).apply_gradients(
        #     grads
        # )
        self.actor_optimizer = tf.keras.optimizers.Adam(
            learning_rate=self.learning_rate
        )
        # ===================================================================== #
        #                              Critic Model                             #
        # ===================================================================== #

        (
            self.critic_state_input,
            self.critic_action_input,
            self.critic_model,
        ) = self.create_critic_model()
        _, _, self.target_critic_model = self.create_critic_model()

        # self.critic_grads = tf.gradients(
        #     self.critic_model.output, self.critic_action_input
        # )  # where we calcaulte de/dC for feeding above

        # # Initialize for later gradient calculations
        # self.sess.run(tf.initialize_all_variables())

    # ========================================================================= #
    #                              Model Definitions                            #
    # ========================================================================= #

    def create_actor_model(self):
        def mapping_to_target_range(x, target_min=0, target_max=3):
            x02 = K.tanh(x) + 1  # x in range(0,2)
            scale = (target_max - target_min) / 2.0
            final = x02 * scale + target_min
            todivide = tf.constant([1, 3, 1, 3], dtype=tf.float32)
            return tf.divide(final, todivide)

        f = tf.function(mapping_to_target_range)
        state_input = Input(shape=self.env.observation_space.shape)
        h1 = Dense(24, activation="relu")(state_input)
        h2 = Dense(48, activation="relu")(h1)
        # just added regularizer, see if still have nan
        h3 = Dense(24, activation="relu", kernel_regularizer="l2")(h2)
        output = Dense(self.env.action_space.shape[0], activation=f)(h3)

        model = Model(inputs=state_input, outputs=output)
        adam = Adam(lr=0.001)
        model.compile(loss="mse", optimizer=adam)
        return state_input, model

    def create_critic_model(self):
        state_input = Input(shape=self.env.observation_space.shape)
        state_h1 = Dense(24, activation="relu")(state_input)
        state_h2 = Dense(48)(state_h1)

        action_input = Input(shape=self.env.action_space.shape)
        action_h1 = Dense(48)(action_input)

        merged = Add()([state_h2, action_h1])
        merged_h1 = Dense(24, activation="relu", kernel_regularizer="l2")(merged)
        output = Dense(1, activation="sigmoid")(merged_h1)
        model = Model(inputs=[state_input, action_input], outputs=output)

        adam = Adam(lr=0.001)
        model.compile(loss="mse", optimizer=adam)
        return state_input, action_input, model

    # ========================================================================= #
    #                               Model Training                              #
    # ========================================================================= #

    def remember(self, cur_state, action, reward, new_state, done):
        self.memory.append([cur_state, action, reward, new_state, done])

    def _train_actor(self, samples):
        for sample in samples:
            cur_state, action, reward, new_state, _ = sample
            cur_state = np.array(cur_state)
            cur_state = tf.constant(cur_state)
            # need change to target model?
            with tf.GradientTape() as tape:
                tape.watch(cur_state)
                predicted_action = self.actor_model(cur_state) #dC/dA
                predicted_reward = self.critic_model([cur_state, predicted_action]) # de/dC
            actor_model_weights = self.actor_model.trainable_weights
            dEdA = tape.gradient(predicted_reward, actor_model_weights)

            # tf.cast(dEdA, tf.float32)
            # dEdA = tf.gradients(predicted_action, actor_model_weights, -dEdC)
            self.actor_optimizer.apply_gradients(zip(dEdA, actor_model_weights))
            # grads = self.sess.run(
            #     self.critic_grads,
            #     feed_dict={
            #         self.critic_state_input: cur_state,
            #         self.critic_action_input: predicted_action,
            #     },
            # )[0]
            # self.sess.run(
            #     self.optimize,
            #     feed_dict={
            #         self.actor_state_input: cur_state,
            #         self.actor_critic_grad: grads,
            #     },
            # )

    def _train_critic(self, samples):
        for sample in samples:
            cur_state, action, reward, new_state, done = sample
            if not done:
                target_action = self.target_actor_model.predict(new_state)
                future_reward = self.target_critic_model.predict(
                    [new_state, target_action]
                )[0][0]
                reward += self.gamma * future_reward
            # print(cur_state, action, reward)
            # cur_state = np.array(cur_state)
            # action = np.array(action)
            reward = np.array([reward])
            # cur_state = cur_state.astype(np.float64)
            # print(cur_state, action, reward)
            self.critic_model.fit([cur_state, action], [reward], verbose=0)

    def train(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return
        samples = random.sample(self.memory, batch_size)
        # print(samples)
        # print("training critic")
        self._train_critic(samples)
        # print("training actor")
        self._train_actor(samples)
        if random.random() < self.tau:  # Updating the target model here
            self.update_target()

    # ========================================================================= #
    #                         Target Model Updating                             #
    # ========================================================================= #

    def _update_actor_target(self):
        actor_model_weights = self.actor_model.get_weights()
        actor_target_weights = self.target_actor_model.get_weights()

        for i in range(len(actor_target_weights)):
            actor_target_weights[i] = actor_model_weights[i]
        self.target_actor_model.set_weights(actor_target_weights)

    def _update_critic_target(self):
        critic_model_weights = self.critic_model.get_weights()
        critic_target_weights = self.target_critic_model.get_weights()

        for i in range(len(critic_target_weights)):
            critic_target_weights[i] = critic_model_weights[i]
        self.target_critic_model.set_weights(critic_target_weights)

    def update_target(self):
        self._update_actor_target()
        self._update_critic_target()

    # ========================================================================= #
    #                              Model Predictions                            #
    # ========================================================================= #

    def act(self, cur_state):
        self.epsilon *= self.epsilon_decay
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        else:
            print("Predicting")
        return self.actor_model.predict(
            cur_state
        )  # This is using the training model not the target model

    # ========================================================================= #
    #                              Model Validations                            #
    # ========================================================================= #
    def validation(self, cur_state):
        return self.target_actor_model.predict(cur_state)

    # ========================================================================= #
    #                              Model Checkpoint                             #
    # ========================================================================= #

    def save_model(self, version):
        self.target_actor_model.save("./saved_model/actor" + version + "/")
        self.target_critic_model.save("./saved_model/critic" + version + "/")
        return

    def reload_model(self, actor_weights, critic_weights):
        self.actor_model.set_weights(actor_weights)
        self.target_actor_model
        pass


def main():
    dfnorm = pd.read_csv("training_data/BTCUSDT_5min_norm.csv")
    dfnorm = dfnorm.iloc[:, 1:]
    df = pd.read_csv("training_data/BTCUSDT_5min.csv")
    df = df.iloc[:, 1:]
    print(df.head(6))
    env = CryptoSingleEnv(df, dfnorm)
    actor_critic = ActorCritic(env)

    num_trials = 2

    cur_state = env.reset()
    action = env.action_space.sample()
    for i in range(num_trials):
        done = False
        while not done:
            env.render()
            cur_state = cur_state.reshape((1, env.observation_space.shape[0]))
            action = actor_critic.act(cur_state)
            action = action.reshape((1, env.action_space.shape[0]))

            print("Action taken:", action)
            new_state, reward, done, _ = env.step(action)
            new_state = new_state.reshape((1, env.observation_space.shape[0]))

            actor_critic.remember(cur_state, action, reward, new_state, done)
            actor_critic.train()

            cur_state = new_state
            # time.sleep(0.1)
        cur_state = env.reset()


if __name__ == "__main__":
    main()
