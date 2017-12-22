import matplotlib
import matplotlib.pyplot as plot

from matplotlib import rcParams
rcParams['font.family']='sans-serif'
rcParams['font.sans-serif']=[
    u'Microsoft Yahei',
    u'SimHei'
] + rcParams['font.sans-serif']

plot.figure()
plot.title(u'新闻')
plot.show()

from matplotlib.font_manager import findfont,FontProperties
font = findfont(FontProperties(family=['sans-serif']))

