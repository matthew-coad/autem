library(tidyverse)


list_battle_files <- function(path)
  list.files(path, "Battle.csv", recursive = TRUE, full.names = TRUE)

read_battle_file <- function(file_name) {
  col_types <- cols(
    simulation = col_character(),
    dataset = col_character(),
    experiment = col_character(),
    version = col_integer(),
    epoch = col_integer(),
    step = col_integer(),
    member_id = col_integer(),
    form_id = col_integer(),
    incarnation = col_integer(),
    event = col_character(),
    time = col_character(),
    fault = col_character(),
    rating = col_double(),
    rating_sd = col_double(),
    ranking = col_double(),
    mature = col_integer(),
    famous = col_integer(),
    contests = col_integer(),
    evaluations = col_integer(),
    standoffs = col_integer(),
    victories = col_integer(),
    defeats = col_integer(),
    data = col_character(),
    accuracy = col_double(),
    top_accuracy = col_double(),
    top_1p_accuracy = col_double(),
    top_5p_accuracy = col_double(),
    top_10p_accuracy = col_double(),
    top_25p_accuracy = col_double(),
    validation_accuracy = col_double(),
    Imputer = col_character(),
    SMP_strategy = col_character(),
    Engineer = col_character(),
    Scaler = col_character(),
    NOR_norm = col_character(),
    BIN_threshold = col_character(),
    Selector = col_character(),
    LPC_scorer = col_character(),
    LPC_percentile = col_double(),
    LVT_threshold = col_double(),
    Reducer = col_character(),
    FIC_tol = col_character(),
    FAG_linkage = col_character(),
    FAG_affinity = col_character(),
    PCA_iterated_power = col_character(),
    Approximator = col_character(),
    RBF_gamma = col_character(),
    NYS_kernel = col_character(),
    NYS_gamma = col_character(),
    NYS_n_components = col_character(),
    Learner = col_character(),
    BNB_alpha = col_character(),
    BNB_fit_prior = col_character(),
    MNB_alpha = col_character(),
    MNB_fit_prior = col_character(),
    CART_criterion = col_character(),
    CART_max_depth = col_character(),
    CART_min_samples_split = col_character(),
    CART_min_samples_leaf = col_character(),
    KNN_n_neighbors = col_character(),
    KNN_weights = col_character(),
    KNN_p = col_character(),
    LSV_penalty = col_character(),
    LSV_loss = col_character(),
    LSV_dual = col_character(),
    LSV_tol = col_character(),
    LSV_C = col_character(),
    LGR_C = col_character(),
    LGR_dual = col_character(),
    RF_criterion = col_character(),
    RF_max_features = col_character(),
    RF_min_samples_split = col_character(),
    RF_min_samples_leaf = col_character(),
    EXT_criterion = col_character(),
    EXT_max_features = col_character(),
    EXT_min_samples_split = col_character(),
    EXT_min_samples_leaf = col_character(),
    irrelevants = col_double(),
    Imputer_importance = col_double(),
    Engineer_importance = col_double(),
    Scaler_importance = col_double(),
    Reducer_importance = col_double(),
    Approximator_importance = col_double(),
    Learner_importance = col_double()
  )
  df <- suppressWarnings(read_csv(file_name, col_types = col_types))
  df
}

clean_battle <- function(df) {
  df$simulation <- factor(df$simulation)
  df$event_time <- lubridate::parse_date_time(df$time, orders = "amd HMS Y")
  df
}

read_battle <- function(path) {
  files <- list_battle_files(path)
  df <- files %>% map_dfr(read_battle_file)
  df
}

baseline_data_filename <- function(baseline_path, baseline_name)
  file.path(baseline_path, baseline_name, "baseline.csv")

read_baseline_file <- function(baseline_path, baseline_name) {
  filename = baseline_data_filename(baseline_path, baseline_name)
  col_types <- cols(
    `Run ID` = col_integer(),
    Flow = col_character(),
    predictive_accuracy = col_double(),
    Hyperparameters = col_character()
  )
  df = read_csv(filename, col_types = col_types, na = c("",NA, "NULL", "null"))
  df
}

build_battle_summary <- function(battle_df) {
  
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

build_accuracy <- function(baseline_path, battle_df) {
  
  summary_df <- build_battle_summary(battle_df)
  
  baseline_accuracy <- function(baseline_name) {
    
    baseline_df <- read_baseline_file(baseline_path, baseline_name) %>% filter(!is.na(predictive_accuracy))
    baseline_accuracy_df <- 
      baseline_df %>%
      mutate(
        experiment = "baseline",
        dataset = baseline_name,
        accuracy = predictive_accuracy
      ) %>%
      select(experiment, dataset, accuracy)
    min_accuracy <- min(baseline_accuracy_df$accuracy)
    max_accuracy <- max(baseline_accuracy_df$accuracy)
    
    battle_accuracy_df <-
      summary_df %>%
      filter(dataset == baseline_name) %>%
      mutate(
        accuracy = rating
      ) %>%
      select(experiment, dataset, accuracy)
    
    accuracy_df <- 
      bind_rows(baseline_accuracy_df, battle_accuracy_df) %>%
      mutate(percentage = percent_rank(accuracy) * 100)
    
    accuracy_df$normal_accuracy <- (accuracy_df$accuracy - min_accuracy) / (max_accuracy - min_accuracy)
    
    accuracy_df
    
  }
  
  baselines <- levels(factor(summary_df$dataset))
  baseline_accuracy_df <- baselines %>% map_dfr(baseline_accuracy)
  baseline_accuracy_df
}

battle_df <- read_battle(simulations_path)
write_rds(battle_df, "battle.RDS")

accuracy_df <- build_accuracy(baseline_path, battle_df)
write_rds(accuracy_df, "accuracy.RDS")
