args <- commandArgs(TRUE)
male_path <- args[[1]]
female_path <- args[[2]]


library(dplyr)

dat <- read.csv(male_path) %>% filter(round == 'AAfinal', !(is.na(predicted_score)))

for(x in 1:100){
  hb <- dat %>% filter(apparatus == 'HB') %>% arrange(-predicted_score) %>% head(x)
  ph <- dat %>% filter(apparatus == 'PH') %>% arrange(-predicted_score) %>% head(x)
  fx <- dat %>% filter(apparatus == 'FX') %>% arrange(-predicted_score) %>% head(x)
  pb <- dat %>% filter(apparatus == 'PB') %>% arrange(-predicted_score) %>% head(x)
  sr <- dat %>% filter(apparatus == 'SR') %>% arrange(-predicted_score) %>% head(x)
  vt <- dat %>% filter(apparatus == 'VT') %>% arrange(-predicted_score) %>% head(x)
  
  common <- inner_join(hb, ph, by=('name'='name')) %>% inner_join(fx, by=('name'='name')) %>%   inner_join(pb, by=('name'='name')) %>% inner_join(sr, by=('name'='name')) %>% inner_join(vt, by=('name'='name'))
  
  if(nrow(common) >= 5){
    break
  }
}

final_men_team <- common %>% mutate(sum_predicted_score = predicted_score.x + predicted_score.y + predicted_score.x.x + predicted_score.y.y + predicted_score.x.x.x + predicted_score.y.y.y) %>% arrange(-sum_predicted_score) %>% head(5) %>% pull(name)




dat <- read.csv(female_path) %>% filter(round == 'AAfinal', !(is.na(predicted_score)))

for(x in 1:100){
  fx <- dat %>% filter(apparatus == 'FX') %>% arrange(-predicted_score) %>% head(x)
  vt <- dat %>% filter(apparatus == 'VT') %>% arrange(-predicted_score) %>% head(x)
  ub <- dat %>% filter(apparatus == 'UB') %>% arrange(-predicted_score) %>% head(x)
  bb <-dat %>% filter(apparatus == 'BB') %>% arrange(-predicted_score) %>% head(x)
  
  common <- inner_join(fx, vt, by=('name'='name')) %>% inner_join(ub, by=('name'='name')) %>%   inner_join(bb, by=('name'='name'))
  
  if(nrow(common) >= 5){
    break
  }
}

final_women_team <- common %>% mutate(sum_predicted_score = predicted_score.x + predicted_score.y + predicted_score.x.x + predicted_score.y.y) %>% arrange(-sum_predicted_score) %>% head(5) %>% pull(name)

final_women_team



