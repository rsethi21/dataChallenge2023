args = commandArgs(TRUE)
train_data = args[[1]]
test_data = args[[2]]
names = args[[3]]
apparatus = args[[4]]
rounds = args[[5]]
output = args[[6]]

print("Open and Clean-up Train Set")
train = read.csv(train_data)
train = train[,colnames(train)[! colnames(train) %in% c("X", "Unnamed..0", "Unnamed..0.1")]]
print("Open and Clean-up Test Set")
test = read.csv(test_data)
test = test[,colnames(test)[! colnames(test) %in% c("X", "Unnamed..0", "Unnamed..0.1")]]

print("Combine Datasets")
all_data = rbind(train, test)

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
