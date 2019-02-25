

configuration_data_filename <- function(benchmark_path)
  file.path(benchmark_path, "Configuration.xlsx")

read_configuration_file <- function(benchmark_path) {
  file_name <- configuration_data_filename(benchmark_path)
  df <- readxl::read_excel(file_name)
  df
}
