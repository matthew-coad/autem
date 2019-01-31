library(shinydashboard)

source("simulations.R")

simulations_path <- "D:\\Documents\\autem\\benchmark\\simulations"

header <- function()
  dashboardHeader(title = "Autem")

sidebar <- function()
  dashboardSidebar(
    sidebarMenu(
      selectInput("simulation", "Simulation", choices = "Loading..."),
      selectInput("kpi", "KPI", choices = "Loading..."),
      menuItem("Progress", tabName = "progress", icon = icon("dashboard")),
      menuItem("Performance", tabName = "performance", icon = icon("dashboard"))
    )
  )

progress_tab <- function()
  tabItem(tabName = "progress",
    fluidRow(
        valueBoxOutput("status_steps")
    ),
          
    fluidRow(
      box(
        title = "Events", status = "primary", solidHeader = TRUE, width = 6,
        plotOutput("population_progress", height = 250)
      ),
      box(
        title = "KPI", status = "primary", solidHeader = TRUE, width = 6,
        plotOutput("kpi_progress", height = 250)
      )
    )
  )

performance_tab <- function()
  tabItem(tabName = "performance",
    fluidRow(
      column(width = 4,
        box(
          title = "Perf Box title", width = NULL, status = "primary",
          "Perf"
        )
      )
    )
  )

body <- function() dashboardBody(tabItems(progress_tab(), performance_tab()))


# We'll save it in a variable `ui` so that we can preview it in the console
ui <- dashboardPage(
  header(),
  sidebar(),
  body()
)

# Preview the UI in the console
shinyApp(ui = ui, server = function(input, output, session) { 
  
  simulations <- reactive({
    load_simulation_choices(simulations_path)
  })
  
  observe({
      updateSelectInput(session, "simulation", choices = simulations())
  })
  
  outline_df <- reactive({
    simulation <- input$simulation
    if (simulation == "Loading...")
      return(NULL)
    outline_df <- load_outline_df(input$simulation)
    outline_df
  })
  
  observe({
    outline_df_value <- outline_df()
    if (is.null(outline_df_value))
      return()
    kpis_df <- outline_df_value %>% dplyr::filter(role == "kpi")
    choices <- kpis_df$label %>% set_names(kpis_df$name)
    updateSelectInput(session, "kpi", choices = choices)
  })

  battle_df <- reactive({
    simulation <- input$simulation
    if (simulation == "Loading...")
      return(NULL)
    battle_df <- load_battle_df(input$simulation)
    battle_df
  })
  
  rank_df <- reactive({
    simulation <- input$simulation
    if (simulation == "Loading...")
      return(NULL)
    df <- load_ranking_df(input$simulation)
    df
  })

  
  progress_df <- reactive({
    battle_df_value <- battle_df()
    if (is.null(battle_df_value))
      return(NULL)
    df <- evaluate_progress_df(battle_df_value)
    df
  })
  
  status <- reactive({
    battle_df_value <- battle_df()
    if (is.null(battle_df_value))
      return(NULL)
    result <- evaluate_status(battle_df_value)
    result
  })
  
  output$status_steps <- renderValueBox({
    current_status <- status()
    valueBox(paste0(current_status$step), "Steps", color = "purple", icon = icon("list"))
  })
  output$population_progress <- renderPlot({population_progress_plot(progress_df())})
  output$kpi_progress <- renderPlot({kpi_progress_plot(rank_df())})

})