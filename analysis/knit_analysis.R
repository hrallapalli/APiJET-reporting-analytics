
dir = getwd()
setwd(dir)

rmarkdown::render("APIJET_flight_deviations_analysis.Rmd",
                  output_file = "APIJET_flight_deviations_analysis.html")