source("process_simulation.R")

simulations_path1 <- "D:\\Documents\\autem\\benchmark\\simulations\\Run_6"
simulations_path2 <- "D:\\Documents\\autem\\benchmark\\simulations\\encoding"
benchmark_path <- "D:\\Documents\\autem\\benchmark"

# Load data
print("Loading battle")
battle_df <- clean_battle(bind_rows(read_battle(simulations_path1), read_battle(simulations_path2)))
datasets <- unique(battle_df$dataset)
baseline_df <- read_baselines(benchmark_path, datasets)
configuration_df <- read_configuration_file(benchmark_path)

# Tranforms data
print("Transforming")
step_detail_df <- build_step_detail(battle_df)
ranking_detail_df <- build_ranking_detail(battle_df)
baseline_detail_df <- build_baseline_details(baseline_df)
baseline_summary_df <- build_baseline_summary(baseline_detail_df)

epoch_detail_df <- build_epoch_details(step_detail_df)

simulation_summary_df <- build_simulation_summary(configuration_df, step_detail_df, ranking_detail_df, baseline_summary_df)

breakdown_df <- build_breakdown()

print("Writing")
write_rds(step_detail_df, "data\\step_detail.RDS")
write_rds(epoch_detail_df, "data\\epoch_detail.RDS")
write_rds(simulation_summary_df, "data\\simulation_summary.RDS")
write_rds(baseline_detail_df, "data\\baseline_detail.RDS")
write_rds(baseline_summary_df, "data\\baseline_summary.RDS")
write_rds(breakdown_df, "data\\breakdown.RDS")
