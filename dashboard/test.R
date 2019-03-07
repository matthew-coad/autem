library(tidyverse)

parameters_df <- read.csv("data\\parameters.csv")
svc_parameters_df <- parameters_df %>% filter(component_name == "sklearn.svm.classes.SVC")
active_parameters <- svc_parameters_df[1,] %>% pull(parameters) %>% as.character() %>% str_split("\\|") %>% .[[1]]
svc_parameters_df <- svc_parameters_df %>% select(!!active_parameters)

unique(svc_parameters_df$coef0)
