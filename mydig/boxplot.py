import matplotlib.pyplot as plt
import numpy as np

data_a = [[92, 86, 89, 79, 81, 85, 90, 89, 81, 90
           ],
          [164, 161, 186, 178, 165, 173, 169, 175, 163, 189
           ],
          [418, 431, 428, 404, 397, 420, 369, 410, 392, 399
           ],
          [399, 439, 434, 382, 403, 469, 440, 434, 472, 402
           ],
          [441, 459, 451, 431, 419, 481, 453, 439, 437, 458
           ],
          [546, 507, 528, 571, 503, 551, 565, 514, 597, 557
           ],
          [424, 425, 407, 441, 421, 418, 430, 413, 431, 411
           ],
          [405, 406, 410, 450, 417, 425, 418, 441, 398, 412
           ],
          [524, 512, 511, 575, 531, 532, 517, 539, 520, 511
           ],
          [886, 591, 397, 382, 419, 786, 605, 581, 413, 599
           ]
          ]

data_b = [[2, 1, 2, 3, 2, 2, 1, 2, 2, 2],
          [3, 3, 3, 2, 2, 2, 2, 3, 3, 2],
          [131, 129, 86, 132, 2, 2, 73, 1, 3, 3],
          [2, 3, 2, 2, 0, 2, 1, 2, 3, 2],
          [2, 3, 2, 1, 2, 2, 2, 2, 3, 2],
          [3, 2, 1, 2, 3, 3, 1, 3, 3, 2],
          [2, 3, 2, 2, 2, 1, 3, 2, 2, 130]
    ,
          [3, 2, 3, 1, 2, 2, 1, 2, 3, 2
           ],
          [2, 3, 2, 2, 2, 3, 2, 3, 3, 1
           ],
          [3, 2, 2, 3, 2, 3, 2, 3, 2, 3
           ]]

data_c = [[100, 110, 75, 79, 31, 38, 66, 70, 34],
          [67, 39, 76, 74, 71, 68, 67, 33, 32, 36],
          [103, 120, 34, 34, 152, 102, 144, 32, 32, 38],
          [31, 37, 30, 36, 32, 32, 31, 36, 42, 32],
          [107, 32, 33, 85, 99, 206, 84, 34, 32, 43],
          [339, 32, 281, 269, 273, 30, 280, 32, 37, 37],
          [36, 34, 32, 30, 298, 34, 37, 32, 32, 32],
          [41, 32, 32, 35, 38, 32, 35, 32, 36, 39],
          [34, 42, 33, 40, 38, 33, 43, 36, 32, 33],
          [31, 31, 34, 30, 33, 34, 38, 35, 37, 38
           ]]

ticks = ['google', 'youtube', 'tmall', 'baidu', 'qq', 'sohu', 'taobao', 'facebook',
         'yahoo', 'amazon']


def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)


plt.figure()
bpl = plt.boxplot(data_a, positions=np.array(range(len(data_a))) * 2.0 - 0.43, sym='', widths=0.3)
bpr = plt.boxplot(data_b, positions=np.array(range(len(data_b))) * 2.0, sym='', widths=0.35)
bpm = plt.boxplot(data_c, positions=np.array(range(len(data_c))) * 2.0 + 0.43, sym='', widths=0.3)

set_box_color(bpl, '#D7191C')
set_box_color(bpr, '#2C7BB6')
set_box_color(bpm, '#636363')

plt.plot([], c='#D7191C', label='myresolver')
plt.plot([], c='#2C7BB6', label='local')
plt.plot([], c='#636363', label='google')

plt.legend()

plt.plot(range(1))
plt.xlabel("Website Name(.com)")
plt.ylabel("Response Time (msec)")

plt.xticks(range(0, len(ticks) * 2, 2), ticks)
plt.xlim(-1, len(ticks) * 1.7)
plt.ylim(0, 650)
plt.tight_layout()
plt.savefig('comparison.jpg')
