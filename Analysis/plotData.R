library(rhdf5)
library(ggplot2)
library(reshape)
library(ggthemes)
library(scales)

#***********************
#	Read in / Prepare Data
#***********************
fp = "../build/output.h5"

azm <- h5read(fp,"/Parameters/listAzm")
mvdr <- h5read(fp,"/Beamforming/MVDR/Magnitude")
bart <- h5read(fp,"/Direction Finding/Bartlett")

#Set limits for plotting
bart = bart + 30
mvdr[mvdr < -30] = -30
bart[bart < -30] = -30
mvdr[mvdr > 2] = 2
bart[bart > 2] = 2

df <- data.frame(azm,mvdr[1:361],bart[1:361])
df_long <- melt(df,id = "azm")

#**********************
#	Plot Data
#**********************
plt <- ggplot(data=df_long,aes(x=azm,y=value,group=variable)) 

# B&W Plots
plt <- plt + geom_line(aes(linetype=variable))
plt <- plt + theme_bw()
plt <- plt + scale_linetype_discrete(name = "Algorithm", labels=c("MVDR","Bartlett"))

#	Color Plots
#plt <- plt + geom_line(aes(color=variable))
#plt <- plt + scale_color_ptol()
#plt <- plt + scale_color_discrete(name = "Algorithm", labels=c("MVDR","Bartlett"))

plt <- plt + labs(title = "1D Beamformed Response")
plt <- plt + labs(x = "Azimuth (deg.)")
plt <- plt + labs(y = "Magnitude (dB)")

#**************************
#	Modify Axes, Title, Theme
#**************************
plt <- plt + theme(plot.title = element_text(size = 14,face="bold",hjust = 0.5))
plt <- plt + theme(axis.title = element_text(size = 10,face="bold"))
plt <- plt + scale_x_continuous(breaks = c(0,90,180,270,360))
plt <- plt + scale_y_continuous(breaks = c(0,-3,-10,-20,-30))

#*******************
#Modify the Legend
#*******************
plt <- plt + theme(legend.title = element_text(size = 10,face="bold"))
plt <- plt + theme(legend.text = element_text(size = 10,face="bold"))
#plt <- plt + theme(legend.position = "right")
plt <- plt + theme(legend.position= c(0.9,0.9))

#Save the plot
ggsave("data1D.pdf")
