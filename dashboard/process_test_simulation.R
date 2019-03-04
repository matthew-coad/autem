
source("process_simulation.R")

simulations_path <- "D:\\Documents\\autem\\benchmark\\simulations\\Run_6"
baseline_path <- "D:\\Documents\\autem\\benchmark\\baselines"

# Load data
print("Loading battle")
battle_df <- clean_battle(read_battle(simulations_path))
datasets <- unique(battle_df$dataset)
baseline_df <- read_baselines(baseline_path, datasets)

# Tranforms data
print("Transforming")
step_detail_df <- build_step_detail(battle_df)
ranking_detail_df <- build_ranking_detail(battle_df)
baseline_detail_df <- build_baseline_details(baseline_df)
baseline_summary_df <- build_baseline_summary(baseline_detail_df)

epoch_summary_df <- build_epoch_summary(step_detail_df)

simulation_summary_df <- build_simulation_summary(step_detail_df, ranking_detail_df, baseline_summary_df)
baseline_detail_df <- build_baseline_details(baseline_df)
normal_baseline_df <- build_normal_baseline(simulation_summary_df, baseline_detail_df)

breakdown_df <- build_breakdown()

print("Writing")
write_rds(step_detail_df, "step_detail.RDS")
write_rds(epoch_summary_df, "epoch_summary.RDS")
write_rds(simulation_summary_df, "simulation_summary.RDS")
write_rds(normal_baseline_df, "normal_baseline.RDS")
write_rds(breakdown_df, "breakdown.RDS")
