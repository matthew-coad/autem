library(tidyverse)


configuration_data_filename <- function(benchmark_path)
  file.path(benchmark_path, "Configuration.xlsx")

read_configuration_file <- function(benchmark_path) {
  file_name <- configuration_data_filename(benchmark_path)
  df <- readxl::read_excel(file_name)
  df
}

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
    famous = col_integer(),
    contests = col_integer(),
    evaluations = col_integer(),
    standoffs = col_integer(),
    victories = col_integer(),
    defeats = col_integer(),
    data = col_character(),
    accuracy = col_double(),
    score = col_double(),
    top_accuracy = col_double(),
    top_1p_accuracy = col_double(),
    top_5p_accuracy = col_double(),
    top_10p_accuracy = col_double(),
    top_25p_accuracy = col_double(),
    validation_accuracy = col_double(),
    dummy_accuracy = col_double(),
    voting_score = col_double(),
    top_voting_score = col_double(),
    choice_predicted_score = col_double(),
    choice_predicted_score_std = col_double(),
    voting_boost  = col_double(),
    voting_duration = col_double(),
    inter_score = col_double(),
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
    PSV_C = col_double(),
    PSV_tol = col_double(),
    PSV_degree = col_double(),
    irrelevants = col_double(),
    Imputer_importance = col_double(),
    Engineer_importance = col_double(),
    Scaler_importance = col_double(),
    Reducer_importance = col_double(),
    Approximator_importance = col_double(),
    Learner_importance = col_double(),
    BIN_num__scaler__threshold = col_double()
  )
  df <- suppressWarnings(read_csv(file_name, col_types = col_types))
  df
}

clean_battle <- function(df) {
  df$simulation <- factor(df$simulation)
  df$version <- factor(df$version)
  df$alive <- factor(df$alive)
  df$final <- factor(df$final)
  df$event_time <- lubridate::parse_date_time(df$time, orders = "amd HMS Y")
  df
}

read_battle <- function(path) {
  files <- list_battle_files(path)
  df <- files %>% map_dfr(read_battle_file)
  df
}

build_step_detail <- function(battle_df) {
  step_df7 <-
    battle_df %>%
    filter(as.integer(as.character(version)) <= 7)
  if (nrow(step_df7) > 0)
    step_df7 <-
      step_df7 %>%
      mutate(
        study = paste0("S", version),
        experiment = paste0(dataset),
        league = famous,
        score = accuracy
      ) 

  step_df8 <-
    battle_df %>%
    filter(as.integer(as.character(version)) == 8)
  if (nrow(step_df8) > 0)  
    step_df8 <- 
      step_df8 %>%
      mutate(
        league = famous,
        score = accuracy
      )
  
  step_df9 <-
    battle_df %>%
    filter(as.integer(as.character(version)) == 9)
  if (nrow(step_df9) > 0)  
    step_df9 <- 
    step_df9 %>%
    mutate(
      score = accuracy
    )
  
  step_df10 <-
    battle_df %>%
    filter(as.integer(as.character(version)) == 10)
  if (nrow(step_df10) > 0)  
    step_df10 <- 
    step_df10 %>%
    mutate(
      choice_predicted_score = NA,
      choice_predicted_score_std = NA
    )
  
  step_df11 <-
    battle_df %>%
    filter(as.integer(as.character(version)) == 11)

  bind_df <- function(step_df, df) {
    if (nrow(df) == 0)
      return (step_df)
    if (is.null(step_df)) {
      return (df)
    }
    bind_rows(step_df, df)
  }
  step_df <- NULL
  step_df <- bind_df(step_df, step_df7)
  step_df <- bind_df(step_df, step_df8)
  step_df <- bind_df(step_df, step_df9)
  step_df <- bind_df(step_df, step_df10)
  step_df <- bind_df(step_df, step_df11)
  step_df <-
    step_df %>%
    mutate(league = factor(league)) %>%
    select(
      study,
      experiment,
      dataset,
      epoch,
      step,
      member_id,
      form_id,
      event,
      event_time,
      fault,
      league,
      alive,
      final,
      choice_predicted_score,
      choice_predicted_score_std,
      score,
      score_std,
      duration,
      Scaler:LGR_dual
    )
  step_df
}

build_ranking_detail <- function(battle_df) {
  step_df7 <-
    battle_df %>%
    filter(!is.na(ranking)) %>%
    filter(as.integer(as.character(version)) <= 7)
  if (nrow(step_df7) > 0)
    step_df7 <- step_df7 %>%
      mutate(
        study = paste0("S", version),
        experiment = paste0(dataset),
        score = accuracy
      )
  
  step_df8 <-
    battle_df %>%
    filter(!is.na(ranking)) %>%
    filter(as.integer(as.character(version)) >= 8 & as.integer(as.character(version)) <= 9)
  if (nrow(step_df8) > 0)
    step_df8 <- step_df8 %>%
      mutate(
        score = accuracy
      )
  
  step_df10 <-
    battle_df %>%
    filter(!is.na(ranking)) %>%
    filter(as.integer(as.character(version)) >= 10)

  bind_df <- function(step_df, df) {
    if (nrow(df) == 0)
      return (step_df)
    if (is.null(step_df)) {
      return (df)
    }
    bind_rows(step_df, df)
  }
  step_df <- NULL
  step_df <- bind_df(step_df, step_df7)
  step_df <- bind_df(step_df, step_df8)
  step_df <- bind_df(step_df, step_df10)

  ranking_df <-
    step_df %>%
    select(
       study,
       experiment,
       ranking,
       # score = rating,
       # Rating is based on entire dataset. In order to validate we need
       # it to based purely on the training dataset
       # Temporarily base it on accuracy with the sd coming from rating.
       # Accuracy is now evaluated using cross validation
       # and its probably okay to use that.
       score, 
       score_sd = rating_sd,
       dummy_score = dummy_accuracy,
       validation_score = validation_accuracy
    )
  ranking_df
}

build_epoch_details <- function(step_detail_df) {
  epoch_summary_df <- step_detail_df %>%
    group_by(study, experiment, epoch) %>%
    summarise(
      start_time = min(event_time),
      end_time = max(event_time),
      duration = lubridate::int_length(lubridate::interval(start_time, end_time)),
      births = sum(event == "birth"),
      faults = sum(event == "fault"),
      deaths = sum(event == "death"),
      nominations = sum(event == "inducted")
    )
  epoch_summary_df
}

baseline_data_filename <- function(benchmark_path, baseline_name)
  file.path(benchmark_path, "baselines", baseline_name, "baseline.csv")

read_baseline_file <- function(benchmark_path, baseline_name) {
  filename = baseline_data_filename(benchmark_path, baseline_name)
  col_types <- cols(
    `Run ID` = col_integer(),
    Flow = col_character(),
    predictive_accuracy = col_double(),
    Hyperparameters = col_character()
  )
  df = read_csv(filename, col_types = col_types, na = c("",NA, "NULL", "null"))
  df
}

read_baselines <- function(benchmark_path, datasets) {
  
  read_dataset_baselines <- function(dataset) {
    baseline_df <- read_baseline_file(benchmark_path, dataset)
    baseline_df$dataset <- dataset
    baseline_df
  }
  
  baseline_df <- datasets %>% map_dfr(read_dataset_baselines)
  baseline_df
}

build_baseline_details <- function(baseline_df) {
  baseline_details_df <- 
    baseline_df %>%
    mutate(baseline_score = predictive_accuracy) %>%
    group_by(dataset) %>%
    mutate(
      baseline_rank = min_rank(baseline_score),
      baseline_percent = percent_rank(baseline_score)
    ) %>%
    ungroup() %>%
    select(dataset, baseline_score, baseline_rank, baseline_percent) %>%
    arrange(dataset, desc(baseline_rank))
  baseline_details_df
}

build_baseline_summary <- function(baseline_details) {
  
  baseline_summary_df <- baseline_details %>%
    group_by(dataset) %>%
    summarise(
      bottom_score = min(baseline_score, na.rm = TRUE),
      top_score = max(baseline_score, na.rm = TRUE)
    )
  
  baseline_summary_df  
}

build_simulation_summary <- function(configuration_df, step_detail_df, ranking_detail_df, baseline_summary_df) {
  
  simulation_summary_df <- 
    step_detail_df %>%
    group_by(study, experiment) %>%
    summarise(
      dataset = first(dataset),
      status = "Complete",
      epochs = max(epoch),
      steps = max(step),
      duration = lubridate::int_length(lubridate::interval(min(event_time), max(event_time)))
    ) %>% 
    ungroup()
  
  simulation_summary_df <-
    simulation_summary_df %>%
    right_join(filter(ranking_detail_df, ranking == 1), by = c("study", "experiment"))
  
  simulation_summary_df <-
    simulation_summary_df %>%
    right_join(baseline_summary_df, by = c("dataset"))
  
  simulation_summary_df <-
    simulation_summary_df %>%
    right_join(configuration_df, by = c("dataset" = "Name"))

  simulation_summary_df <- 
    simulation_summary_df %>% 
    mutate(
      baseline_bottom_score = bottom_score,
      baseline_top_score = top_score,
      progress_bottom_score = bottom_score,
      progress_top_score = baseline_top_score,
      progress = (score - progress_bottom_score) / (progress_top_score - progress_bottom_score),
      progress_sd = score_sd / (progress_top_score - progress_bottom_score)
    ) %>%
    select(
      study,
      experiment,
      dataset,
      status,
      duration, 
      epochs, 
      steps, 
      score,
      score_sd,
      dummy_score,
      validation_score,
      baseline_bottom_score,
      baseline_top_score,
      progress_bottom_score,
      progress_top_score,
      progress,
      progress_sd
    )
  
  simulation_summary_df <- 
    simulation_summary_df %>%
    mutate(
      study = if_else(!is.na(study), study, "None"),
      experiment = if_else(!is.na(experiment), experiment, dataset),
      status = if_else(!is.na(status), status, "Missing")
    )
  simulation_summary_df
}

build_dataset_summary <- function(configuration_df) {
  output_df <- 
    configuration_df %>%
    select(
      dataset = Name,
      classes = NumberOfClasses,
      features = NumberOfFeatures,
      instances = NumberOfInstances,
      incomplete = NumberOfInstancesWithMissingValues,
      missing = NumberOfMissingValues
    )
  output_df
}

build_breakdown <- function() {
  tibble::tibble(breakdown = c("Learner", "Scaler", "Selector", "Reducer", "Approximator"))
}



