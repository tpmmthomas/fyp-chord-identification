from collections import deque
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input, Flatten
from tensorflow.keras.optimizers import Adam
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import math
from itertools import combinations
from datetime import datetime
from music21 import *
import random

# For the reward function:
# if correct segmentation: output +1 #(change of roughness)
# if incorrect segmentation: output -1#(correct change of roughness in the next segmentation)
# if correct do nothing : output +1
# if incorrect do nothing: output -1 #(correct change of roughness)
# if illegal: output 0


class SegmentationEnv(Env):  # Fit one particular coin first
    def __init__(self, pieces):
        # Preprocess the pieces
        self.notes = []
        self.offset = []
        self.beat = []
        self.duration = []
        self.octave = []
        self.correct_offset = []
        #         self.beatchanges = []
        for piece in pieces:
            print(piece)
            xnotes = []
            xoffset = []
            xbeat = []
            xduration = []
            xoctave = []
            xcoroffset = []
            c = converter.parse(piece)
            post = c.flattenParts().flat
            for note in post.notes:
                duration = note.duration.quarterLength
                offset = note.offset
                beat = note.beat
                if note.lyric is not None and note.offset != 0:
                    xcoroffset.append(note.offset // 1)
                allnotes = list(note.pitches)
                for note1 in allnotes:
                    xnotes.append(note1.name)
                    xoffset.append(offset)
                    xbeat.append(beat)
                    xduration.append(duration)
                    xoctave.append(note1.octave)
            self.notes.append(xnotes)
            self.offset.append(xoffset)
            self.beat.append(xbeat)
            self.duration.append(xduration)
            self.octave.append(xoctave)
            self.correct_offset.append(xcoroffset)
            #             xbeatchange = {}
        #             for ts in post.recurse().getElementsByClass(meter.TimeSignature):
        #                 assert ts.denominator in [2,4,8]
        #                 if ts.denominator == 2:
        #                     xbeatchange[ts.offset] = 2
        #                 elif ts.denominator == 4:
        #                     xbeatchange[ts.offset] = 1
        #                 else:
        #                     xbeatchange[ts.offset] = 0.5
        #             self.beatchanges.append(xbeatchange)

        # Actions: Remain segment (0), segment (1)
        self.action_space = Discrete(2)

        # Observations: First dim 12 pitch classes, Second dim Octave (1-7), Value is total duration.
        self.observation_space = Box(
            low=np.zeros((12, 7), dtype=np.float32),
            high=np.ones((12, 7), dtype=np.float32),
        )

        # internal state: check where the time currently is
        self.current_piece = 0
        self.current_noteoffset = 0
        self.notelistfirst = 0
        self.notelistlast = 0
        self.latestbeatfirst = 0
        self.latestbeatlast = 0
        self.state = np.zeros((12, 7))

        # save segmentation for rendering purposes
        self.determined_offset = []

    def step(self, action):
        # Calculating reward
        if action == 0:  # do nothing
            is_segment = False
            if (
                self.current_noteoffset not in self.correct_offset[self.current_piece]
            ):  # correct
                reward = 1
            else:
                reward = max(-self.change_in_roughness() / 20, -1)
        else:  # segmentation
            is_segment = True
            if self.current_noteoffset == 0:  # illegal operations
                reward = -0.7
            else:
                self.determined_offset.append(
                    (self.current_piece, self.current_noteoffset)
                )
                if self.current_noteoffset in self.correct_offset[self.current_piece]:
                    reward = 1
                else:
                    reward = -1
        # determine new obs state
        if is_segment and self.current_noteoffset != 0:
            self.notelistfirst = self.latestbeatfirst
        done = False
        if self.latestbeatlast == len(
            self.beat[self.current_piece]
        ):  # Finished a piece
            self.current_piece += 1
            if self.current_piece == len(self.notes):
                done = True
            else:
                done = False
                self.current_noteoffset = 0
                self.notelistfirst = 0
                self.notelistlast = 0
                self.latestbeatfirst = 0
                self.latestbeatlast = 0
        if not done:
            self.current_noteoffset = self.offset[self.current_piece][
                self.latestbeatlast
            ]
            currentbeat = self.beat[self.current_piece][self.latestbeatlast] // 1
            currentindex = self.latestbeatlast + 1
            self.latestbeatfirst = self.latestbeatlast
            while (
                len(self.beat[self.current_piece]) > currentindex
                and self.beat[self.current_piece][currentindex] // 1 == currentbeat
            ):
                currentindex += 1
            self.notelistlast = currentindex
            self.latestbeatlast = currentindex
        info = {}
        return self.staterender(done), reward, done, info

    def render(self):
        print("Current piece:", self.current_piece)
        print("Current notelist:", self.notelistfirst, self.notelistlast)
        for segment in self.determined_offset:
            print(segment)
        return

    def change_in_roughness(self):
        def roughness(notes):
            """
            Calculate the Roughness of notes according to sum of ideal ratio N+M
            Reference: https://www.researchgate.net/publication/276905584_Measuring_Musical_Consonance_and_Dissonance
            """

            def interval_to_ratio(interval):
                interval_ratio_mapping = {
                    0: 1 + 1,
                    1: 18 + 17,
                    2: 9 + 8,
                    3: 6 + 5,
                    4: 5 + 4,
                    5: 4 + 3,
                    6: 17 + 12,
                    7: 3 + 2,
                    8: 8 + 5,
                    9: 5 + 3,
                    10: 16 + 9,
                    11: 17 + 9,
                    12: 2 + 1,
                }
                interval_pitch_mapping = {
                    1: 0,
                    2: 2,
                    3: 4,
                    4: 5,
                    5: 7,
                    6: 9,
                    7: 11,
                    8: 12,
                }
                ans = interval_pitch_mapping[int(interval[-1])]
                if int(interval[-1]) in [4, 5, 8]:
                    intname = interval[:-1]
                    if intname == "dd":
                        ans -= 2
                    elif intname == "d":
                        ans -= 1
                    elif intname == "A":
                        ans += 1
                    elif intname == "AA":
                        ans += 2
                else:
                    intname = interval[:-1]
                    if intname == "m":
                        ans -= 1
                    elif intname == "d":
                        ans -= 2
                    elif intname == "A":
                        ans += 1
                    elif intname == "AA":
                        ans += 2
                ans = ans % 12
                return interval_ratio_mapping[ans]

            ans = 0
            for combo in combinations(notes, 2):
                n1 = note.Note(combo[0])
                n2 = note.Note(combo[1])
                xinterval = interval.Interval(noteStart=n1, noteEnd=n2)
                ans += interval_to_ratio(xinterval.semiSimpleName)
            return ans / len(notes) if len(notes) != 0 else 0

        notelist1 = []
        for i in range(self.notelistfirst, self.latestbeatfirst):
            notelist1.append(
                self.notes[self.current_piece][i]
                + str(self.octave[self.current_piece][i])
            )
        notelist2 = notelist1.copy()
        for i in range(self.latestbeatfirst, self.latestbeatlast):
            notelist2.append(
                self.notes[self.current_piece][i]
                + str(self.octave[self.current_piece][i])
            )
        notelist1 = list(dict.fromkeys(notelist1))
        notelist2 = list(dict.fromkeys(notelist2))
        return abs(roughness(notelist2) - roughness(notelist1))

    def staterender(self, done):
        pitch_to_index = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
        obsarray = np.zeros((12, 7))
        notelist = []
        if done:
            return obsarray
        for idx in range(self.notelistfirst, self.notelistlast):
            current_note = self.notes[self.current_piece][idx]
            notelist.append(current_note)
            current_duration = self.duration[self.current_piece][idx]
            current_octave = self.octave[self.current_piece][idx]
            pitchindex = pitch_to_index[current_note[0]]
            current_note = current_note[1:]
            if current_note == "#":
                pitchindex += 1
            elif current_note == "##":
                pitchindex += 2
            elif current_note == "-":
                pitchindex -= 1
            elif current_note == "--":
                pitchindex -= 2
            pitchindex = pitchindex % 12
            if current_octave < 1 or current_octave > 7:
                continue
            current_octave -= 1
            obsarray[pitchindex][current_octave] += current_duration
            obsarray[pitchindex][current_octave] = min(
                20, obsarray[pitchindex][current_octave]
            )
        #         print(notelist)
        obsarray = obsarray / 20
        return obsarray

    def reset(self):
        self.current_piece = 0
        self.current_noteoffset = 0
        self.notelistfirst = 0
        self.notelistlast = 0  # exclusive
        self.latestbeatfirst = 0
        self.latestbeatlast = 0  # exclusive
        currentbeat = self.beat[self.current_piece][self.latestbeatlast] // 1
        currentindex = self.latestbeatlast + 1
        while (
            len(self.beat[self.current_piece]) > currentindex
            and self.beat[self.current_piece][currentindex] // 1 == currentbeat
        ):
            currentindex += 1
        self.notelistlast = currentindex
        self.latestbeatlast = currentindex
        return self.staterender(False)


import glob

training_pieces = []
for piece in glob.glob("../musicxml(notated)/*.mxl"):
    training_pieces.append(piece)
testing_pieces = []
for piece in glob.glob("../review/*.musicxml"):
    testing_pieces.append(piece)


from stable_baselines3 import DQN

env = SegmentationEnv(training_pieces)

# model = DQN("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=100000, log_interval=4)
# model.save("segmenatation_1")


class DQNSolver:
    def __init__(
        self,
        env,
        n_episodes=1000,
        max_env_steps=None,
        gamma=1.0,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_log_decay=0.995,
        alpha=0.01,
        alpha_decay=0.01,
        batch_size=64,
    ):
        self.env = env
        self.memory = deque(maxlen=100000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_log_decay
        self.alpha = alpha
        self.alpha_decay = alpha_decay
        self.n_episodes = n_episodes
        self.batch_size = batch_size
        if max_env_steps is not None:
            self.env._max_episode_steps = max_env_steps

        # Init model
        state_input = Input(shape=self.env.observation_space.shape)
        h1 = Flatten()(state_input)
        h2 = Dense(128, activation="tanh")(h1)
        h3 = Dense(64, activation="tanh")(h2)
        output = Dense(2, activation="linear")(h3)
        self.model = Model(inputs=state_input, outputs=output)
        adam = Adam(lr=self.alpha, decay=self.alpha_decay)
        self.model.compile(loss="mse", optimizer=adam)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state, epsilon):
        state = state.reshape((1, 12, 7))
        return (
            self.env.action_space.sample()
            if (np.random.random() <= epsilon)
            else np.argmax(self.model.predict(state))
        )

    def get_epsilon(self, t):
        return max(
            self.epsilon_min,
            min(self.epsilon, 1.0 - math.log10((t + 1) * self.epsilon_decay)),
        )

    def replay(self, batch_size):
        x_batch, y_batch = [], []
        minibatch = random.sample(self.memory, min(len(self.memory), batch_size))
        for state, action, reward, next_state, done in minibatch:
            state = state.reshape((1, 12, 7))
            next_state = next_state.reshape((1, 12, 7))
            y_target = self.model.predict(state)
            y_target[0][action] = (
                reward
                if done
                else reward + self.gamma * np.max(self.model.predict(next_state)[0])
            )
            x_batch.append(state[0])
            y_batch.append(y_target[0])

        self.model.fit(
            np.array(x_batch), np.array(y_batch), batch_size=len(x_batch), verbose=0
        )
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def run(self):
        for e in range(self.n_episodes):
            done = False
            state = env.reset()
            while not done:
                action = self.choose_action(state, self.get_epsilon(e))
                next_state, reward, done, _ = self.env.step(action)
                self.remember(state, action, reward, next_state, done)
                state = next_state
            self.replay(self.batch_size)
        return e


agent = DQNSolver(env)
agent.run()

env = SegmentationEnv(testing_pieces)
obs = env.reset()
while True:
    obs = obs.reshape((1, 12, 7))
    action = np.argmax(agent.model.predict(obs))
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        break
