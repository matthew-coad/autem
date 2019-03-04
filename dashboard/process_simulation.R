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
    dummy_accuracy = col_double(),
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
  df$version <- factor(df$version)
  df$event_time <- lubridate::parse_date_time(df$time, orders = "amd HMS Y")
  df
}

read_battle <- function(path) {
  files <- list_battle_files(path)
  df <- files %>% map_dfr(read_battle_file)
  df
}

build_step_detail <- function(battle_df) {
  step_df <-
    battle_df %>%
    select(
      experiment = version,
      configuration = experiment, 
      dataset,
      epoch,
      step,
      member_id,
      event,
      event_time,
      fault,
      mature,
      star = famous,
      alive,
      final,
      evaluations,
      accuracy,
      duration,
      dummy_accuracy,
      Scaler:LGR_dual
    )
  step_df
}

build_ranking_detail <- function(battle_df) {
  
  ranking_df <-
    battle_df %>%
    filter(!is.na(ranking)) %>%
     select(
       experiment = version, 
       configuration = experiment, 
       dataset, 
       ranking,
       rating, 
       rating_sd, 
       dummy_accuracy,
       validation_accuracy)
  ranking_df
}

build_epoch_summary <- function(step_detail_df) {
  epoch_summary_df <- step_detail_df %>%
    group_by(experiment, configuration, dataset, epoch) %>%
    summarise(
      start_time = min(event_time),
      end_time = max(event_time),
      duration_secs = lubridate::int_length(lubridate::interval(start_time, end_time)),
      births = sum(event == "birth"),
      faults = sum(event == "fault"),
      deaths = sum(event == "death"),
      nominations = sum(event == "inducted")
    )
  epoch_summary_df
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

read_baselines <- function(baseline_path, datasets) {
  
  read_dataset_baselines <- function(dataset) {
    baseline_df <- read_baseline_file(baseline_path, dataset)
    baseline_df$dataset <- dataset
    baseline_df
  }
  
  baseline_df <- datasets %>% map_dfr(read_dataset_baselines)
  baseline_df
}

build_baseline_details <- function(baseline_df) {
  baseline_details_df <- 
    baseline_df %>%
    mutate(baseline_accuracy = predictive_accuracy) %>%
    group_by(dataset) %>%
    mutate(
      baseline_rank = min_rank(baseline_accuracy),
      baseline_percent = percent_rank(baseline_accuracy)
    ) %>%
    ungroup() %>%
    select(dataset, baseline_accuracy, baseline_rank, baseline_percent) %>%
    arrange(dataset, desc(baseline_rank))
  baseline_details_df
}

build_baseline_summary <- function(baseline_details) {
  
  baseline_summary_df <- baseline_details %>%
    group_by(dataset) %>%
    summarise(
      min_accuracy = min(baseline_accuracy),
      max_accuracy = max(baseline_accuracy)
    )
  
  baseline_summary_df  
}


build_simulation_summary <- function(step_detail_df, ranking_detail_df, baseline_summary_df) {
  
  simulation_summary_df <- 
    step_detail_df %>%
    group_by(experiment, configuration, dataset) %>%
    summarise(
      epochs = max(epoch),
      steps = max(step),
      run_time_secs = lubridate::int_length(lubridate::interval(min(event_time), max(event_time)))
    ) %>% 
    ungroup()
  
  simulation_summary_df$Status <- "Complete"
  simulation_summary_df <-
    simulation_summary_df %>%
    right_join(filter(ranking_detail_df, ranking == 1), by = c("experiment", "configuration", "dataset"))
  
  simulation_summary_df <-
    simulation_summary_df %>%
    right_join(baseline_summary_df, by = c("dataset"))
  
  simulation_summary_df <- 
    simulation_summary_df %>% 
    mutate(
      min_baseline_accuracy = min_accuracy,
      max_baseline_accuracy = max_accuracy,
      normal_delta = dummy_accuracy,
      normal_scale = max_baseline_accuracy - dummy_accuracy,
      normal_rating = (rating - normal_delta) / normal_scale,
      normal_rating_sd = rating_sd / normal_scale,
      normal_dummy_accuracy = (dummy_accuracy - normal_delta) / normal_scale,
      normal_validation_accuracy = (validation_accuracy - normal_delta) / normal_scale,
      normal_min_baseline_accuracy = (min_baseline_accuracy - normal_delta) / normal_scale,
      normal_max_baseline_accuracy = (max_baseline_accuracy - normal_delta) / normal_scale
    ) %>%
    select(
      experiment, 
      configuration, 
      dataset, 
      epochs, 
      steps, 
      run_time_secs, 
      status = Status, 
      rating,
      rating_sd,
      dummy_accuracy,
      validation_accuracy,
      min_baseline_accuracy,
      max_baseline_accuracy,
      normal_delta,
      normal_scale,
      normal_rating,
      normal_rating_sd,
      normal_dummy_accuracy,
      normal_validation_accuracy,
      normal_min_baseline_accuracy,
      normal_max_baseline_accuracy
    )
  simulation_summary_df
}

build_normal_baseline <- function(simulation_summary_df, baseline_detail_df) {
  simulation_summary_df %>%
    right_join(baseline_detail_df, by = c("dataset")) %>%
    mutate(
      normal_baseline_accuracy = (baseline_accuracy - normal_delta) / normal_scale
    ) %>%
    select(experiment, configuration, dataset, baseline_accuracy, dummy_accuracy, baseline_rank, baseline_percent, normal_baseline_accuracy) %>%
    filter(normal_baseline_accuracy >= 0)
}

build_breakdown <- function() {
  tibble::tibble(breakdown = c("event", "mature", "star",  "Learner", "Scaler", "Selector", "Reducer", "Approximator"))
}



