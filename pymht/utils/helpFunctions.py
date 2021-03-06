from __future__ import print_function
import numpy as np
import logging

log = logging.getLogger(__name__)

def _getBestTextPosition(normVelocity, **kwargs):
    DEBUG = kwargs.get('debug', False)
    compassHeading = np.arctan2(normVelocity[0], normVelocity[1]) * 180. / np.pi
    compassHeading = (compassHeading + 360.) % 360.
    assert compassHeading >= 0, str(compassHeading)
    assert compassHeading <= 360, str(compassHeading)
    quadrant = int(2 + (compassHeading - 90) // 90)
    assert quadrant >= 1, str(quadrant)
    assert quadrant <= 4, str(quadrant)
    assert type(quadrant) is int
    if DEBUG: print("Vector {0:} Heading {1:5.1f} Quadrant {2:}".format(normVelocity, compassHeading, quadrant))
    # return horizontal_alignment, vertical_alignment
    if quadrant == 1:
        return 'right', 'top'
    elif quadrant == 2:
        return 'right', 'bottom'
    elif quadrant == 3:
        return 'left', 'bottom'
    elif quadrant == 4:
        return 'left', 'top'
    else:
        print('_getBestTextPosition failed. Returning default')
        return 'center', 'center'


def binomial(n, k):
    return 1 if k == 0 else (0 if n == 0 else binomial(n - 1, k) + binomial(n - 1, k - 1))


def plotVelocityArrowFromNode(nodes, **kwargs):
    def recPlotVelocityArrowFromNode(node, stepsLeft):
        if node.predictedStateMean is not None:
            plotVelocityArrow(node)
        if stepsLeft > 0 and (node.parent is not None):
            recPlotVelocityArrowFromNode(node.parent, stepsLeft - 1)

    for node in nodes:
        recPlotVelocityArrowFromNode(node, kwargs.get("stepsBack", 1))


def printScanList(scanList):
    for index, measurement in enumerate(scanList):
        print("\tMeasurement ", index, ":\t", end='', sep='')
        measurement.print()


def printHypothesesScore(targetList):
    def recPrint(target, targetIndex):
        if target.trackHypotheses is not None:
            for hyp in target.trackHypotheses:
                recPrint(hyp, targetIndex)

    for targetIndex, target in enumerate(targetList):
        print("\tTarget: ", targetIndex,
              "\tInit", target.initial.position,
              "\tPred", target.predictedPosition(),
              "\tMeas", target.measurement, sep="")


def backtrackMeasurementNumbers(selectedNodes, steps=None):
    def recBacktrackNodeMeasurements(node, measurementBacktrack, stepsLeft=None):
        if node.parent is not None:
            if stepsLeft is None:
                measurementBacktrack.append(node.measurementNumber)
                recBacktrackNodeMeasurements(node.parent, measurementBacktrack)
            elif stepsLeft > 0:
                measurementBacktrack.append(node.measurementNumber)
                recBacktrackNodeMeasurements(
                    node.parent, measurementBacktrack, stepsLeft - 1)

    measurementsBacktracks = []
    for node in selectedNodes:
        measurementNumberBacktrack = []
        recBacktrackNodeMeasurements(node, measurementNumberBacktrack, steps)
        measurementNumberBacktrack.reverse()
        measurementsBacktracks.append(measurementNumberBacktrack)
    return measurementsBacktracks


def writeElementToFile(path, element):
    import xml.etree.ElementTree as ET
    import os
    (head, tail) = os.path.split(path)
    if not os.path.isdir(head):
        os.makedirs(head)
    tree = ET.ElementTree(element)
    tree.write(path)