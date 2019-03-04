source("battle.r")
source("baseline.r")


simulations_path <- "D:\\Documents\\autem\\benchmark\\simulations\\Run_6"
baseline_path <- "D:\\Documents\\autem\\benchmark\\baselines"

battle_df <- read_battle(simulations_path)

write_rds(battle_df, "Battle.RDS")

build_summary <- function(battle_df) {
  
  error_df <- 
    battle_df %>%
    filter(fault != "None") %>%
    group_by(dataset, experiment, version, fault) %>%
    summarise(n = n()) %>%
    ungroup() %>%
    mutate(fault = str_sub(fault, 1, 80)) %>%
    select(dataset, experiment, version, n, fault)
  
  error_count_df <-
    error_df %>%
    group_by(dataset, experiment, version) %>%
    summarise(n_error = sum(n)) %>%
    ungroup()
  
  summary_df <-
    battle_df %>%
    filter(ranking == 1) %>%
    group_by(dataset, experiment, version) %>%
    left_join(error_count_df, by = c("dataset","experiment", "version")) %>%
    arrange(experiment, dataset, version) %>%
    select(experiment, dataset, version, rating, rating_sd, top_accuracy, top_5p_accuracy, validation_accuracy, n_error) %>%
    ungroup()
  
  summary_df
}



baseline_accuracy <- function(baseline_name) {
  
  baseline_df <- read_baseline_file(baseline_path, baseline_name) %>%
    filter(!is.na(predictive_accuracy))
  
  baseline_accuracy_df <- 
    baseline_df %>%
    mutate(
      experiment = "baseline",
      dataset = baseline_name,
      version = 0,
      accuracy = predictive_accuracy,
      accuracy_sd = NA,
      validation_accuracy = NA
    ) %>%
    select(experiment, dataset, version, accuracy, accuracy_sd, validation_accuracy)
  min_accuracy <- min(baseline_accuracy_df$accuracy)
  max_accuracy <- max(baseline_accuracy_df$accuracy)
  
  battle_accuracy_df <-
    summary_df %>%
    filter(dataset == baseline_name) %>%
    mutate(
      accuracy = rating,
      accuracy_sd = rating_sd
    ) %>%
    select(experiment, dataset, version, accuracy, accuracy_sd, validation_accuracy)
  
  accuracy_df <- 
    bind_rows(baseline_accuracy_df, battle_accuracy_df) %>%
    mutate(percentage = percent_rank(accuracy) * 100)
  
  accuracy_df$normal_accuracy <- (accuracy_df$accuracy - min_accuracy) / (max_accuracy - min_accuracy)
  accuracy_df$normal_accuracy_sd <- accuracy_df$accuracy_sd / (max_accuracy - min_accuracy)
  accuracy_df$normal_validation_accuracy <- (accuracy_df$validation_accuracy - min_accuracy) / (max_accuracy - min_accuracy)
  
  accuracy_df
  
}



baseline_accuracy_df <- baselines %>% map_dfr(baseline_accuracy)
write_rds(baseline_accuracy_df, "Baseline.RDS")

