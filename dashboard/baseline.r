


#def baseline_directory(baseline_name):
#  return baselines_directory().joinpath(baseline_name)

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
  df = read_csv(filename, col_types = col_types)
  df
}

baseline_accuracy <- function(baseline_name) {
  
  baseline_df <- read_baseline_file(baseline_path, baseline_name)
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


#def baseline_data_filename(baseline_name):
#  return baseline_directory(baseline_name).joinpath("baseline.csv")

# def load_baseline_data(baseline_name):
#   filename = baseline_data_filename(baseline_name)
# df = pandas.read_csv(filename)
# return df
# 
# def get_baseline_stats(baseline_name):
#   df = load_baseline_data(baseline_name)
# n_runs = df.shape[0]
# scores = df.predictive_accuracy
# median_score = np.median(scores)
# max_score = np.max(scores)
# min_score = np.min(scores)
# top_1p = np.percentile(scores, 99)
# top_5p = np.percentile(scores, 95)
# top_10p = np.percentile(scores, 90)
# top_qtr = np.percentile(scores, 75)
# 
# stats = {
#   "n_runs": n_runs,
#   "median_score": median_score,
#   "max_score": max_score,
#   "min_score": min_score,
#   "top_1p": top_1p,
#   "top_5p": top_5p,
#   "top_10p": top_10p,
#   "top_qtr": top_qtr
# }
# return stats
