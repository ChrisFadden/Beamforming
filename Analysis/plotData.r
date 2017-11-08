library(rhdf5)
library(ggplot2)

#Access Dataset of specific frequency

azm <- h5read("../build/weights.h5","/listAzm")
mag <- h5read("../build/weights.h5","/Magnitude")
soi <- h5read("../build/weights.h5","/SOI")
hpp <- h5read("../build/weights.h5","/HPP")

df = data.frame(azm,mag)

ggplot(df,aes(azm,mag)) + geom_line() + 
	geom_vline(xintercept=soi,linetype = "dashed") + 
	ggtitle("Directed Array Performance") +	
	labs(x = "Azimuth (Degrees)", y = "Magnitude (dB)") +	
	theme_bw() + theme(plot.title = element_text(hjust = 0.5, face = "bold"),
	axis.title = element_text(face = "bold")) + 
	scale_x_continuous(breaks = c(0,90,180,270,soi,hpp[1],hpp[2]))

H5close()
