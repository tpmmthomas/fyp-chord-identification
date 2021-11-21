def intersection(seg1, seg2):
    if seg1[0] > seg2[0]:
        tmp = seg1
        seg1 = seg2
        seg2 = tmp
    seg1_a, seg1_b = seg1
    seg2_a, seg2_b = seg2
    if seg2_b < seg1_b:
        return seg2_b - seg2_a
    elif seg2_a < seg1_b:
        return seg1_b - seg2_a
    else:
        return 0


def dhd(seg1, seg2):
    """
        dhd: Directional Hamming Distance
        Input: 
        seg1 -> A list of segments, in the form [(a,b),(c,d)]
        seg2 -> Same as seg1
        Returns: the DHD of seg1 vs seg2 
    """
    total = 0
    diff = 0
    for seg in seg1:
        maxOverlap = 0
        for segx in seg2:
            tmp = intersection(seg, segx)
            if tmp > maxOverlap:
                maxOverlap = tmp
            elif tmp == 0 and maxOverlap != 0:
                break
        seglen = seg[1] - seg[0]
        diff += seglen - maxOverlap
        total += seglen
    return diff/total


def segmentation_quality(seg1, seg2):
    return 1 - max(dhd(seg1, seg2), dhd(seg2, seg1))

