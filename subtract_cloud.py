#!/usr/bin/env python

import georasters as gr
import numpy as np
import matplotlib.pyplot as plt


T1 = r"./output/inyo_bcets/20141108_mojave_bcet/20141108_mojave_bcet_B1.tif"
T2 = r"./output/inyo_bcets/20140225_mojave_bcet/20140225_mojave_bcet_B1.tif"
T3 = r"./output/inyo_bcets/20151026_mojave_bcet/20151026_mojave_bcet_B1.tif"
T4 = r"./output/inyo_bcets/20160302_mojave_bcet/20160302_mojave_bcet_B1.tif"
T5 = r"./output/inyo_bcets/20160926_mojave_bcet/20160926_mojave_bcet_B1.tif"
T6 = r"./output/inyo_bcets/20170727_mojave_bcet/20170727_mojave_bcet_B1.tif"
T7 = r"./output/inyo_bcets/20170913_mojave_bcet/20170913_mojave_bcet_B1.tif"

T1_gr = gr.from_file(T1)
T2_gr = gr.from_file(T2)
T3_gr = gr.from_file(T3)
T4_gr = gr.from_file(T4)
T5_gr = gr.from_file(T5)
T6_gr = gr.from_file(T6)
T7_gr = gr.from_file(T7)

