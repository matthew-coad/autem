library(tidyverse)
library(readr)

test_path <- "D:\\Documents\\autem\\benchmark\\simulations\\balance-scale_1_select"

load_simulations_df <- function(path) {
  dirs <- list.dirs(path, full.names = FALSE) %>% setdiff("")
  
  load_simulation_dir <- function(dir) {
    simulation <- tibble::tibble(
      name = dir,
      path = file.path(path, dir)
    )
  }
  df <- purrr::map_dfr(dirs, load_simulation_dir)
  df
}

load_simulation_choices <- function(path) {
  df <- load_simulations_df(path)
  choices <- df$path %>% set_names(df$name)
  choices
}

load_outline_df <- function(path) {
  outline_path <- file.path(path, "Outline.csv")
  col_types <- cols(
    name = col_character(),
    dataset = col_character(),
    role = col_character(),
    label = col_character()
  )
  df <- suppressMessages(read_csv(outline_path, col_names = TRUE, col_types = col_types))
  df
}


# Load battle data for a simulation
load_battle_df <- function(path) {
  
  files <- list.files(path, "Battle*")
  
  load_battle_file <- function(filename) {
    battle_path <- file.path(path, filename)
    df <- suppressMessages(read_csv(battle_path))
    df
  }
  
  df <- purrr::map_dfr(files, load_battle_file)
  df
}

# Load ranking data for a simulation
load_ranking_df <- function(path) {
  
  files <- list.files(path, "Rank*")
  
  load_rank_file <- function(filename) {
    rank_path <- file.path(path, filename)
    df <- suppressMessages(read_csv(rank_path))
    df
  }
  
  df <- purrr::map_dfr(files, load_rank_file)
  df
}

# Generate simulation status report from the battle data
evaluate_status <- function(battle_df) {
  steps <- max(battle_df$step)
  list(step = steps)
}

# Generate progress report
evaluate_progress_df <- function(battle_df) {
  df <- battle_df %>%
    mutate(
      alive = cumsum(n_alive), 
      mature = cumsum(n_mature), 
      famous = cumsum(n_famous),
      score = 0
    ) %>% 
    select(step, alive, mature, famous, score)
  df
}

population_progress_plot <- function(progress_df) {
  plot <- progress_df %>%
    ggplot(aes(x = step)) +
    geom_line(aes(y = alive, color = "alive")) +
    geom_line(aes(y = mature, color = "mature")) +
    geom_line(aes(y = famous, color = "famous")) +
    xlab("Step") +
    ylab("Population")
  plot
}

kpi_progress_plot <- function(ranking_df) {
  plot <- ranking_df %>%
    ggplot(aes(x = step)) +
    geom_point(aes(y = score), na.rm = TRUE) +
    xlab("Step") +
    ylab("Score")
  plot
}

top_configuration <- function(ranking_df, outline_df) {
  last_rank <- ranking_df %>% filter(row_number()==n()) %>% tidyr::gather("name")
  properties <- outline_df %>% filter(dataset == "ranking", role == "configuration")
  last_rank %>% dplyr::inner_join(properties, by="name") %>% select(label, value)
}

top_score <- function(ranking_df) {
  last_rank <- ranking_df %>% filter(row_number()==n())
  last_rank %>% pull(score)
}

