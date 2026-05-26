from matplotlib import pyplot as plt

plt.style.use('Solarize_Light2')
# plt.xkcd()
plt.minorticks_on()

dev_x = list(range(25,35+1))
dev_y = [38496, 42000, 46752, 49320, 53200,
         56000, 62316, 64928, 67317, 68748, 73752]
plt.plot(dev_x,dev_y,color = "#043a4b",linestyle= '--',linewidth=3,label = 'All Devs')

py_dev_y = [45372, 48876, 53850, 57287, 63016,
            65998, 70003, 70000, 71496, 75370, 83640]
plt.plot(dev_x,py_dev_y,color = '#adad3b',linewidth=3,label = 'Python')

js_dev_y = [37810, 43515, 46823, 49293, 53437,
            56373, 62375, 66674, 68745, 68746, 74583]
plt.plot(dev_x,js_dev_y,color = "#000000",linestyle ='--',label = 'JS')

plt.xlabel('Ages')
plt.ylabel('Median Salary(USD)')
plt.title('Median Salary(USD) by Ages')
plt.legend()
plt.tight_layout()
plt.grid(True,which='minor',color = "#393838",alpha= 0.4)
plt.grid(True,which='major',color = "#01181E",linewidth=2,alpha=0.7)
plt.savefig('plot.png')

plt.show()