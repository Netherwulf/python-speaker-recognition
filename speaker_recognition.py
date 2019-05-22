#!/usr/bin/env python3

import os
import sys
import itertools
import glob
import argparse
from utils import read_wav
from interface import ModelInterface


def get_args():
    desc = "Speaker Recognition Command Line Tool"
    epilog = """
Wav files in each input directory will be labeled as the basename of the directory.
Note that wildcard inputs should be *quoted*, and they will be sent to glob.glob module.
Examples:
    Train (enroll a list of person named person*, and mary, with wav files under corresponding directories):
    ./speaker_recognition.py -t enroll -i "/tmp/person* ./mary" -m model.out
    Predict (predict the speaker of all wav files):
    ./speaker_recognition.py -t predict -i "./*.wav" -m model.out
"""
    parser = argparse.ArgumentParser(description=desc, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-t', '--task',
                        help='Task to do. Either "enroll" or "predict"',
                        required=True)

    parser.add_argument('-i', '--input',
                        help='Input Files(to predict) or Directories(to enroll)',
                        required=True)

    parser.add_argument('-m', '--model',
                        help='Model file to save(in enroll) or use(in predict)',
                        required=True)

    ret = parser.parse_args()
    return ret


def task_enroll(input_dirs, output_model):
    m = ModelInterface()
    input_dirs = [os.path.join(k) for k in input_dirs.strip().split(',')]
    # dirs = itertools.chain(*(glob.glob(d) for d in input_dirs))
    dirs = [d for d in input_dirs]

    files = []
    if len(dirs) == 0:
        print("No valid directory found!")
        sys.exit(1)

    for d in dirs:
        label = os.path.basename(d.rstrip('/'))
        wavs = glob.glob(d + '/*.wav')

        if len(wavs) == 0:
            print("No wav file found in %s" % (d))
            continue
        for wav in wavs:
            try:
                fs, signal = read_wav(wav)
                m.enroll(label, fs, signal)
                print("wav %s has been enrolled" % (wav))
            except Exception as e:
                print(wav + " error %s" % (e))

    m.train()
    m.dump(output_model)


def task_predict(input_files, input_model):
    m = ModelInterface.load(input_model)
    fs, signal = read_wav(input_files)
    label, score = m.predict(fs, signal)
    print("label", '->', label, ", score->", score)
    result = [label, score]
    return result


if __name__ == "__main__":
    global args
    args = get_args()

    task = args.task
    if task == 'enroll':
        task_enroll(args.input, args.model)
    elif task == 'predict':
        task_predict(args.input, args.model)
