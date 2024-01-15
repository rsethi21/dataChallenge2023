args = commandArgs(TRUE)
data = args[[1]]
names = args[[2]]
apparatus = args[[3]]
rounds = args[[4]]
output = args[[5]]

print("Open and Clean-up Dataset")
all_data = read.csv(data)
all_data = all_data[,colnames(all_data)[! colnames(all_data) %in% c("X", "Unnamed..0", "Unnamed..0.1")]]

print("Training Model...")
model = lm(Score ~ Country + Apparatus + Round + days_till_paris + rate_of_change + Location + names + average_apparatus_rank, data=all_data)

print("Creating Prediction DataFrame")
i = 1
country = "USA"
paris = 0
loc = "Paris, France"
rounds = read.csv(rounds)$round
names = read.csv(names)$Name
apparatus = read.csv(apparatus)$apparatus
output_names <- c()
output_rounds <- c()
output_apparatus <- c()
output_score <- c()
for (n in names) {
  for (r in rounds) {
    for (a in apparatus) {
      index = as.numeric(rownames(all_data[all_data$Apparatus == a & all_data$names == n & all_data$Round == r,]))[1]
      average_app_rank = all_data[index,"average_apparatus_rank"]
      average_rof = all_data[index,"rate_of_change"]
      output_names <- c(output_names, n)
      output_rounds <- c(output_rounds, r)
      output_apparatus <- c(output_apparatus, a)
      output_score <- c(output_score, predict(model, data.frame(Country=country, Round=r, Apparatus=a, Location=loc, days_till_paris=paris, names=n, rate_of_change=average_rof, average_apparatus_rank= average_app_rank)))
    }
  }
  i = i + 1
  cat("\r",paste0(round(i / length(names) * 100), '% completed'))
}

print("Saving Predictions to CSV")
frame = data.frame(name=output_names, round=output_rounds, apparatus=output_apparatus, predicted_score=output_score)
write.csv(frame, output)
