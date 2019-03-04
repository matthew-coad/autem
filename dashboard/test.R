normal_rating <- 0.86
normal_baseline_df %>% filter(dataset == "adult", baseline_accuracy <= normal_rating) %>% pull(baseline_percent) %>% max()
