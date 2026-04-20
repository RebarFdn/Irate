import plotly.express as px, os
from palmerpenguins import load_penguins
from ipyleaflet import Map
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import output_widget, render_widget
from pathlib import Path, PurePath
from htmltools import TagList, div

#config
BASE_PATH:Path = Path(__file__).parent.parent.parent.parent
VIDEO_PATH:Path = BASE_PATH / 'Videos'
# Data Source 
penguins = load_penguins()
videos:list = [ item for item in os.listdir(VIDEO_PATH) if '.mp4' in item ]

v1 = VIDEO_PATH / videos[1]
v2 = "https://youtu.be/ncsR8yZ4oXk"

app_ui = ui.page_fluid(
    ui.page_navbar(
    ui.nav_panel(
         ui.input_dark_mode()
         
    ),
    
    ui.nav_panel("Industry Rates",
            "Industry Rates",        
            ui.page_fillable(
                # Add Font Awesome CSS in the head section
                ui.tags.head(
                    ui.tags.link(
                        rel="stylesheet",
                        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css",
                    )
                ),

                # First card
                ui.card(
                    ui.card_header("Action Link Demo"),
                    # Create an action link with an icon
                    ui.input_action_button("action_button", "Action"),  
                    ui.output_text("counter"),
                    ui.input_action_link(
                        id="demo_link",
                        label="Click Me!",
                        icon=ui.tags.i(class_="fa-solid fa-shield-halved"),
                    ),
                    ui.output_text("link_clicks"),
                    full_screen=True,
                    height="300px",
                    id="card1",
                ),

            ),
            ui.card(
                    ui.card_header("Action Link Demo"),
            ),
            ui.card(
                    ui.card_header("Video Path"),
                    f"Video Path: {v1.as_posix()}",
            ),
            ui.card(
                ui.card_header("Videos"),
                f"{videos}",
                ui.hr(),
                ui.tags.video(
                    src=".www/bread.mp4",
                    type="video/mp4",
                    controls=True,
                    auto_play=True,
                    width = "50%",
                    style="max-width: 600px;"

                    )
            ),
            


            
        ),
    ui.nav_panel("Your Rates", 
            ui.page_fluid(
        # Add Font Awesome CSS in the head
        ui.tags.head(
            ui.tags.link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css",
            )
        ),
        # Main layout
        ui.layout_column_wrap(
            ui.card(
                ui.card_header("Action Button Examples"),
                # Basic button with width parameter
                ui.input_action_button("show", "Show modal dialog"),
                ui.input_action_button(id="btn1", label="Basic Button", width="200px"),
                ui.output_text("click_count_btn1"),
                ui.br(),  # Add spacing
                # Button with icon and disabled state
                ui.input_action_button(
                    id="btn2",
                    label="Disabled Button with Icon",
                    icon=ui.tags.i(class_="fa-solid fa-shield-halved"),
                    disabled=True,
                ),
                ui.output_text("click_count_btn2"),
                ui.br(),  # Add spacing
                # Button with custom class and style attributes
                ui.input_action_button(
                    id="btn3",
                    label="Styled Button",
                    class_="btn-success",
                    style="margin-top: 20px;",
                ),
                ui.output_text("click_count_btn3"),
            ),
            width="100%",
        ),
        )
        ), 
    ui.nav_panel('Maps',
            ui.page_fluid(output_widget("map"))  
        ),
    ui.nav_panel('Data Model Example',
            ui.page_fluid(
            ui.input_slider("n", "Number of bins", 1, 100, 20),
            output_widget("plot"),  
            ) ,
            ui.page_fluid(
                ui.h2("Palmer Penguins"),
                ui.output_data_frame("penguins_df"),  
            ),
            ui.page_fluid(
                ui.h2("Palmer Penguins"),
                ui.output_data_frame("penguins_dt"),  
            )
        ),
    ui.nav_panel('Chat',
    ui.page_fillable(
    ui.panel_title("Vidi Chat"),
    ui.chat_ui("chat"),  
        fillable_mobile=True,
        )   
    
    ),
    title= "Vidi" ,
    id="page1",
    bg="#e8b87d"

    ),
    

)
def server( input: Inputs, output: Outputs, session: Session):

    # Create a chat instance and display it
    chat = ui.Chat(id="chat")

    @render.text
    @reactive.event(input.action_button)
    def counter():
        return f"{input.action_button()}"

    @render.text
    def click_count_btn1():
        return f"Button 1 clicks: {input.btn1() or 0}"

    @render.text
    def click_count_btn2():
        return f"Button 2 clicks: {input.btn2() or 0}"

    @render.text
    def click_count_btn3():
        return f"Button 3 clicks: {input.btn3() or 0}"

    @render.text
    def link_clicks():
        count = input.demo_link() or 0
        return f"The link has been clicked {count} times"

    @render_widget  
    def map():
        return Map(center=(50.6252978589571, 0.34580993652344), zoom=3)
    
    @render_widget  
    def plot():  
        scatterplot = px.histogram(
            data_frame=penguins,
            x="body_mass_g",
            nbins=input.n()
            
        ).update_layout(
            title={"text": "Penguin Mass", "x": 0.5},
            yaxis_title="Count",
            xaxis_title="Body Mass (g)",
        )
        return scatterplot 

    @render.data_frame  
    def penguins_df():
        return render.DataGrid(penguins)  

    @render.data_frame  
    def penguins_dt():
        return render.DataTable(penguins)  

    # Define a callback to run when the user submits a message
    @chat.on_user_submit  
    async def handle_user_input(user_input: str):  
        # Simply echo the user's input back to them
        await chat.append_message(f"You said: {user_input}") 

    @reactive.effect
    @reactive.event(input.show)
    def _():
        m = ui.modal(  
            "This is a somewhat important message.",  
            title="Somewhat important message",  
            easy_close=True,  
        )  
        ui.modal_show(m)  






app = App(app_ui, server )