import customtkinter as ctk
import re
import json
from pathlib import Path

ELEMENTS_FILE = Path("PeriodicTableJSON.json")
with open(ELEMENTS_FILE, "r", encoding="utf-8") as file:
    ELEMENTS = {el["symbol"]: el["atomic_mass"] for el in json.load(file)["elements"]}

BLUE_COLOUR = "#2e8bc0"
DARK_BLUE_COLOUR = "#145da0"
GRAY_COLOUR = "#F1F1F1"
DARK_GRAY_COLOUR = "gray50"
BACKGROUND_COLOUR = "#d2d2d2"

class ReactionYieldPredictor:
    def __init__(self, window):
        self.window = window
        window.title("Reaction Yield Calculator")
        window.configure(fg_color=BACKGROUND_COLOUR)
        window.geometry("660x330")

        self.variables()
        self.header_text()
        self.ask_calculation_mode()

    def variables(self):
        self.title_frame = None
        self.radiobutton_frame = None
        self.radiobutton_check_button = None
        self.dropdown_menu_frame = None

        self.percent_yield_frame = None
        self.percent_yield_calculation_frame = None
        self.percent_yield_results_frame = None
        self.percent_yield_calculations_description_frame = None
        self.percent_yield_formula_outer_frame = None
        self.calculate_percent_yield_button = None

        self.theoretical_yield_frame = None
        self.theoretical_yield_calculation_frame = None
        self.theoretical_yield_results_frame = None
        self.theoretical_yield_calculations_description_frame = None
        self.theoretical_yield_formula_outer_frame = None
        self.calculate_theoretical_yield_button = None

        self.limiting_reagent_frame = None
        self.limiting_reagent_calculation_frame = None
        self.limiting_reagent_results_frame = None
        self.limiting_reagent_calculations_description_frame = None
        self.limiting_reagent_formula_outer_frame = None
        self.calculate_limiting_reagent_button = None

        self.number_of_reagents_frame = None
        self.types_of_reagents_outer_frame = None
        # self.types_of_reagents_inner_frame
        self.buttons_frame = None

        self.number_of_products_frame = None
        self.types_of_products_outer_frame = None
        # self.types_of_products_inner_frame

        self.equation_outer_frame = None
        self.reagent_results_outer_frame = None
        self.product_results_outer_frame = None
        self.percent_yield_results_outer_frame = None

        self.mode_choice = ctk.StringVar(value="0")
        self.quick_calculation_options_choice = ctk.StringVar()

        self.number_reagents = ctk.StringVar(value="0")
        self.reagent_stoichiometry_entries = []
        self.reagent_formula_entries = []
        self.reagent_mass_entries = []
        self.reagents = []

        self.number_products = ctk.StringVar(value="0")
        self.product_stoichiometry_entries = []
        self.product_formula_entries = []
        self.product_mass_entries = []
        self.products = []

        self.main_product = ctk.IntVar(value=-1)

        self.information_frame = None
        self.error_label = None
        self.errors_frame = None
        self.reagents_error_label = None
        self.products_error_label = None

    def header_text(self):
        self.title_frame = ctk.CTkFrame(self.window, fg_color=BLUE_COLOUR, corner_radius=15)
        self.title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 0), padx=20)

        title = ctk.CTkLabel(self.title_frame, fg_color=BLUE_COLOUR, text="Reaction Yield Calculator", text_color="white",
                         font=("Arial", 30), anchor="w", justify="left")
        title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 1))

        description = ctk.CTkLabel(self.title_frame, fg_color=BLUE_COLOUR, text="Calculate Percent Yield and Reaction Efficiency",
                               text_color="white", font=("Arial", 20), anchor="w", justify="left")
        description.grid(row=1, column=0, sticky="w", padx=20, pady=(1, 15))

    def ask_calculation_mode(self):
        self.radiobutton_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15)
        self.radiobutton_frame.grid(row=1, column=0, sticky="ew", pady=(10, 10), padx=20)

        mode_label = ctk.CTkLabel(self.radiobutton_frame, text="Choose what mode of the calculator you prefer...",
                                       text_color="black", font=("Arial", 15, "bold"))
        mode_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 5), padx=20)

        already_know_radiobutton = ctk.CTkRadioButton(self.radiobutton_frame, fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                      text="Quick Mode: Already know the numbers? "
                                                           "Just enter actual & theoretical yield.", text_color="black",
                                                      font=("Arial", 13), variable=self.mode_choice, value="quick")
        already_know_radiobutton.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 10), padx=20)

        does_not_know_radiobutton = ctk.CTkRadioButton(self.radiobutton_frame, fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                       text="Detailed Mode: Enter your reaction and "
                                                            "starting masses, and we’ll calculate everything for you.",
                                                       text_color="black", font=("Arial", 13), variable=self.mode_choice, value="detailed")
        does_not_know_radiobutton.grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 10), padx=20)

        self.radiobutton_check_button = ctk.CTkButton(self.radiobutton_frame, command=self.check_mode_selection,
                                                      fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                      text="Select", font=("Arial", 12, "bold"))
        self.radiobutton_check_button.grid(row=3, column=0, columnspan=2, pady=(10, 10), padx=20)

    def check_mode_selection(self):
        if self.mode_choice.get() == "quick":
            self.window.geometry("760x220")
            self.remove_radiobuttons()
            self.ask_quick_calculation_mode()

        elif self.mode_choice.get() == "detailed":
            self.window.geometry("1170x600")
            self.remove_radiobuttons()
            self.ask_reagent_count()
            self.ask_product_count()

        else:
            if self.radiobutton_check_button is not None:
                self.radiobutton_check_button.destroy()
                setattr(self, "radiobutton_check_button", None)

            no_option_selected = ctk.CTkLabel(self.radiobutton_frame, text="Please select an option.",
                                              text_color="red", font=("Arial", 15, "italic"))
            no_option_selected.grid(row=3, column=0, sticky="w", pady=(10, 10), padx=20)

            radiobutton_check_button = ctk.CTkButton(self.radiobutton_frame, command=self.check_mode_selection,
                                                     fg_color="#2e8bc0", hover_color="#145da0", text="Select",
                                                     font=("Arial", 12, "bold"))
            radiobutton_check_button.grid(row=3, column=1, sticky="e", pady=(10, 10), padx=20)

    def remove_radiobuttons(self):
        if self.radiobutton_frame is not None:
            self.radiobutton_frame.destroy()
            setattr(self, "radiobutton_frame", None)

    def ask_quick_calculation_mode(self):
        self.dropdown_menu_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=725, height=90)
        self.dropdown_menu_frame.grid(row=1, column=0, columnspan=2, sticky="n", pady=(10, 5), padx=20)
        self.dropdown_menu_frame.grid_propagate(False)

        quick_mode_label = ctk.CTkLabel(self.dropdown_menu_frame, text="I want to calculate the...",
                                        text_color="black", font=("Arial", 15, "bold"))
        quick_mode_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 5), padx=20)

        quick_calculation_options = ["percent yield", "theoretical yield", "limiting reagent"]
        self.quick_calculation_options_choice.set("Select a calculation")

        quick_options_dropdown = ctk.CTkComboBox(self.dropdown_menu_frame, width=500, command=self.check_quick_calculation_mode,
                                                 fg_color="white", border_color=BLUE_COLOUR, text_color="black", font=("Arial", 13),
                                                 button_color=BLUE_COLOUR, button_hover_color=DARK_BLUE_COLOUR,
                                                 dropdown_fg_color="white", dropdown_hover_color=GRAY_COLOUR,
                                                 dropdown_text_color="black", variable=self.quick_calculation_options_choice,
                                                 values=quick_calculation_options)
        quick_options_dropdown.grid(row=1, column=0, sticky="w", pady=(5, 10), padx=20)

        reset_quick_calculation_button = ctk.CTkButton(self.dropdown_menu_frame, command=self.reset_quick_calculation_mode, fg_color=BLUE_COLOUR,
                                     text="Reset", font=("Arial", 10, "bold"))
        reset_quick_calculation_button.grid(row=1, column=1, sticky="w", pady=(5, 10), padx=20)

    def reset_quick_calculation_mode(self):
        self.window.state("normal")
        self.window.geometry("660x330")
        self.remove_dropdown_menu()
        self.remove_yield_frames()
        self.ask_calculation_mode()

    def check_quick_calculation_mode(self, choice):
        if choice == "percent yield":
            self.window.state("zoomed")
            self.remove_yield_frames()
            self.percent_yield()
            self.show_percent_yield_results_frames()
            self.show_general_information()

        elif choice == "theoretical yield":
            self.window.state("zoomed")
            self.remove_yield_frames()
            self.theoretical_yield()
            self.show_theoretical_yield_results_frames()
            self.show_general_information()

        elif choice == "limiting reagent":
            self.window.state("zoomed")
            self.remove_yield_frames()
            self.limiting_reagent()
            self.show_limiting_reagent_results_frames()
            self.show_general_information()

    def percent_yield(self):
        self.percent_yield_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=320, height=330)
        self.percent_yield_frame.grid(row=2, column=0, rowspan=2, sticky="w", pady=(10, 10), padx=20)
        self.percent_yield_frame.grid_propagate(False)

        percent_yield_title = ctk.CTkLabel(self.percent_yield_frame, fg_color="white", text="Reaction Yield Calculator",
                                                       text_color="black", font=("Arial", 18), anchor="w")
        percent_yield_title.grid(row=0, column=0, sticky="w", pady=(15, 3), padx=15)

        percent_yield_description_frame = ctk.CTkFrame(self.percent_yield_frame, fg_color=BLUE_COLOUR, corner_radius=15)
        percent_yield_description_frame.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=20)

        percent_yield_description_text = ctk.CTkLabel(percent_yield_description_frame, fg_color=BLUE_COLOUR,
                                                      text="Calculate the percent yield of your chemical reaction to see "
                                                           "how efficient it was. This tells you how much product you "
                                                           "actually got compared to the maximum amount you could have made.",
                                                      text_color="white", font=("Arial", 11), wraplength=260, justify="left")
        percent_yield_description_text.pack(pady=(15, 15), padx=(15, 8))

        self.percent_yield_calculation_frame = ctk.CTkFrame(self.percent_yield_frame, fg_color=GRAY_COLOUR, corner_radius=15)
        self.percent_yield_calculation_frame.grid(row=2, column=0, sticky="w", pady=(10, 15), padx=15)

        self.actual_yield_mass = ctk.CTkEntry(self.percent_yield_calculation_frame, width=245, height=25, corner_radius=8,
                                              fg_color="white", placeholder_text="Actual yield (g)",
                                              placeholder_text_color=DARK_GRAY_COLOUR, text_color="black", font=("Arial", 10),
                                              justify="left")
        self.actual_yield_mass.pack(pady=(20, 10), padx=(15, 15))

        self.theoretical_yield_mass = ctk.CTkEntry(self.percent_yield_calculation_frame, width=245, height=25, corner_radius=8,
                                                   fg_color="white", placeholder_text="Theoretical yield (g)",
                                                   placeholder_text_color=DARK_GRAY_COLOUR, font=("Arial", 10), text_color="black",
                                                   justify="left")
        self.theoretical_yield_mass.pack(pady=(10, 15), padx=(15, 15))

        self.calculate_percent_yield_button = ctk.CTkButton(self.percent_yield_calculation_frame, width=245, command=self.check_percent_yield_inputs,
                                                       fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR, text="Calculate", font=("Arial", 10))
        self.calculate_percent_yield_button.pack(pady=(1, 15), padx=20)

    def show_percent_yield_results_frames(self):
        self.percent_yield_results_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=360, height=150)
        self.percent_yield_results_frame.grid(row=2, column=1, sticky="w", pady=(10, 10), padx=20)
        self.percent_yield_results_frame.grid_propagate(False)

        percent_yield_calculation_results_title = ctk.CTkLabel(self.percent_yield_results_frame, fg_color="white",
                                                               text="Calculation Results", text_color="black", font=("Arial", 18),
                                                               anchor="w", justify="left")
        percent_yield_calculation_results_title.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=15)

        self.percent_yield_calculations_description_frame = ctk.CTkFrame(self.percent_yield_results_frame, fg_color=GRAY_COLOUR,
                                                                         corner_radius=15, width=320, height=80)
        self.percent_yield_calculations_description_frame.grid(row=1, column=0, sticky="w", pady=(5, 15), padx=20)
        self.percent_yield_calculations_description_frame.grid_propagate(False)

        percent_yield_analysis_title = ctk.CTkLabel(self.percent_yield_calculations_description_frame, text="Percent Yield Analysis:",
                                                    text_color="black", font=("Arial", 15, "bold"), justify="left")
        percent_yield_analysis_title.grid(row=0, pady=(15, 0), padx=20)

        self.percent_yield_formula_outer_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=360, height=150)
        self.percent_yield_formula_outer_frame.grid(row=3, column=1, sticky="w", pady=(10, 10), padx=20)
        self.percent_yield_formula_outer_frame.grid_propagate(False)

        calculation_formula_title = ctk.CTkLabel(self.percent_yield_formula_outer_frame, text="Essential Formula",
                                                 text_color="black", fg_color="white", font=("Arial", 18), anchor="w")
        calculation_formula_title.grid(row=0, sticky="w", padx=15, pady=(15, 5))

        percent_yield_formula_inner_frame = ctk.CTkFrame(self.percent_yield_formula_outer_frame, fg_color=BLUE_COLOUR,
                                                         corner_radius=15, width=330, height=80)
        percent_yield_formula_inner_frame.grid(row=1, sticky="w", pady=(5, 15), padx=15)
        percent_yield_formula_inner_frame.grid_propagate(False)

        percent_yield_calculation_formula_title = ctk.CTkLabel(percent_yield_formula_inner_frame, fg_color=BLUE_COLOUR,
                                                               text="Percent Yield", text_color="white",
                                                               font=("Arial", 14, "bold"), anchor="w")
        percent_yield_calculation_formula_title.grid(row=0, column=0, sticky="w", pady=(15, 0), padx=15)

        percent_yield_calculation_formula_description = ctk.CTkLabel(percent_yield_formula_inner_frame, fg_color=BLUE_COLOUR,
                                                                     text="% Yield = (Actual/Theoretical) × 100%",
                                                                     text_color="white", font=("Arial", 14), anchor="w")
        percent_yield_calculation_formula_description.grid(row=1, column=0, sticky="w", pady=(0, 20), padx=15)

    def check_percent_yield_inputs(self):
        try:
            actual_mass = float(self.actual_yield_mass.get())
            theoretical_mass = float(self.theoretical_yield_mass.get())

            if theoretical_mass <= 0 or actual_mass < 0:
                self.show_percentage_yield_error("Mass values must be positive and theoretical > 0.")
                return

            self.remove_error_message()
            self.reset_calculate_percent_yield_button()
            self.calculate_percent_yield_button = ctk.CTkButton(self.percent_yield_calculation_frame, width=245,
                                                                command=self.check_percent_yield_inputs,
                                                                fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                                text="Calculate", font=("Arial", 10))
            self.calculate_percent_yield_button.pack(pady=(1, 15), padx=20)
            self.calculate_percent_yield()

        except ValueError:
            self.show_percentage_yield_error("Please enter a valid numeric mass.")

    def calculate_percent_yield(self):
        self.reset_percent_yield_calculation_frames()
        actual_mass = float(self.actual_yield_mass.get())
        theoretical_mass = float(self.theoretical_yield_mass.get())
        percent_yield_value = float((actual_mass/theoretical_mass) * 100)

        percent_yield_results_text = [f"{percent_yield_value:.2f}%"]
        if percent_yield_value <= 70:
            percent_yield_results_text.append(f"Lower yield - consider optimizing conditions")
            result_colour = "#A50801"
        elif 70 < percent_yield_value <= 90:
            percent_yield_results_text.append(f"Good yield for most organic reactions")
            result_colour = "#D4A502"
        elif 90 < percent_yield_value <= 100:
            percent_yield_results_text.append(f"Excellent yield! Very efficient reaction")
            result_colour = "#136F05"
        elif percent_yield_value > 100:
            percent_yield_results_text.append(f"Warning: Yield over 100% may indicate experimental error")
            result_colour = "#A50801"

        percent_yield_results_text = "\n".join(percent_yield_results_text)

        self.percent_yield_results_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=360, height=150)
        self.percent_yield_results_frame.grid(row=2, column=1, sticky="w", pady=(10, 10), padx=20)
        self.percent_yield_results_frame.grid_propagate(False)

        percent_yield_calculation_results_title = ctk.CTkLabel(self.percent_yield_results_frame, fg_color="white",
                                                               text="Calculation Results", text_color="black", font=("Arial", 18),
                                                               anchor="w", justify="left")
        percent_yield_calculation_results_title.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=15)

        self.percent_yield_calculations_description_frame = ctk.CTkFrame(self.percent_yield_results_frame, fg_color=GRAY_COLOUR,
                                                                         corner_radius=15, width=320, height=80)
        self.percent_yield_calculations_description_frame.grid(row=1, column=0, sticky="w", pady=(5, 15), padx=20)
        self.percent_yield_calculations_description_frame.grid_propagate(False)

        percent_yield_analysis_title = ctk.CTkLabel(self.percent_yield_calculations_description_frame, text="Percent Yield Analysis:",
                                                    text_color="black", font=("Arial", 15, "bold"), justify="left", anchor="w")
        percent_yield_analysis_title.grid(row=0, sticky="w", pady=(10, 0), padx=20)
        percent_yield_calculations_description = ctk.CTkLabel(self.percent_yield_calculations_description_frame,
                                                              text=percent_yield_results_text, text_color=result_colour,
                                                              font=("Arial", 11), justify="left")
        percent_yield_calculations_description.grid(row=1, pady=(5, 15), padx=20)

    def show_percentage_yield_error(self, message):
        self.remove_error_message()
        self.reset_calculate_percent_yield_button()

        self.calculate_percent_yield_button = ctk.CTkButton(self.percent_yield_calculation_frame, width=245,
                                                            command=self.check_percent_yield_inputs,
                                                            fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                            text="Calculate", font=("Arial", 10))
        self.calculate_percent_yield_button.pack(pady=(1, 2), padx=20)
        self.error_label = ctk.CTkLabel(self.percent_yield_calculation_frame, text=message, text_color="red",
                                        fg_color=GRAY_COLOUR, font=("Arial", 10, "italic", "bold"))
        self.error_label.pack(pady=0)

    def reset_calculate_percent_yield_button(self):
        if self.calculate_percent_yield_button is not None:
            self.calculate_percent_yield_button.destroy()
            self.calculate_percent_yield_button = None

    def reset_percent_yield_calculation_frames(self):
        for widget_name in ["percent_yield_results_frame", "percent_yield_calculations_description_frame"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def theoretical_yield(self):
        self.theoretical_yield_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, height=420, width=320)
        self.theoretical_yield_frame.grid(row=2, column=0, rowspan=2, sticky="w", pady=(10, 10), padx=20)
        self.theoretical_yield_frame.grid_propagate(False)

        theoretical_yield_calculator_title = ctk.CTkLabel(self.theoretical_yield_frame, fg_color="white",
                                                          text="Theoretical Yield Calculator", text_color="black",
                                                          font=("Arial", 18), anchor="w")
        theoretical_yield_calculator_title.grid(row=0, column=0, sticky="w", pady=(15, 3), padx=15)

        theoretical_yield_description_frame = ctk.CTkFrame(self.theoretical_yield_frame, fg_color=BLUE_COLOUR, corner_radius=15)
        theoretical_yield_description_frame.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=20)

        theoretical_yield_calculator_description = ctk.CTkLabel(theoretical_yield_description_frame, fg_color=BLUE_COLOUR,
                                                                text="Find the theoretical yield, which is the largest "
                                                                          "amount of product you can possibly make from your "
                                                                          "starting materials in a perfect chemical reaction. "
                                                                          "This is a key step before calculating percent yield.",
                                                                text_color="white", font=("Arial", 11), wraplength=260, justify="left")
        theoretical_yield_calculator_description.pack(pady=(15, 15), padx=(15, 8))

        self.theoretical_yield_calculation_frame = ctk.CTkFrame(self.theoretical_yield_frame, fg_color=GRAY_COLOUR, corner_radius=15)
        self.theoretical_yield_calculation_frame.grid(row=2, column=0, sticky="w", pady=(10, 3), padx=15)

        self.limiting_reagent_mass = ctk.CTkEntry(self.theoretical_yield_calculation_frame, width=245, height=25, corner_radius=8,
                                                  fg_color="white", placeholder_text="Limiting reagent (g)",
                                                  placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                                  font=("Arial", 10), justify="left")
        self.limiting_reagent_mass.pack(pady=(20, 10), padx=(15, 15))

        self.molar_mass_reagent = ctk.CTkEntry(self.theoretical_yield_calculation_frame, width=245, height=25, corner_radius=8,
                                               fg_color="white", placeholder_text="Molar Mass of Reagent (g/mol)",
                                               placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                               font=("Arial", 10), justify="left")
        self.molar_mass_reagent.pack(pady=(10, 10), padx=(15, 15))

        self.molar_mass_product = ctk.CTkEntry(self.theoretical_yield_calculation_frame, width=245, height=25, corner_radius=8,
                                               fg_color="white", placeholder_text="Molar Mass of Product (g/mol)",
                                               placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                               font=("Arial", 10), justify="left")
        self.molar_mass_product.pack(pady=(10, 10), padx=(15, 15))

        self.stoichiometric_ratio = ctk.CTkEntry(self.theoretical_yield_calculation_frame, width=245, height=25, corner_radius=8,
                                                 fg_color="white", placeholder_text="Stoichiometric Ratio (1:n)",
                                                 placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                                 font=("Arial", 10), justify="left")
        self.stoichiometric_ratio.pack(pady=(10, 10), padx=(15, 15))

        self.calculate_theoretical_yield_button = ctk.CTkButton(self.theoretical_yield_calculation_frame, width=245,
                                                           command=self.check_theoretical_yield_inputs,
                                                           fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                           text="Calculate", font=("Arial", 10))
        self.calculate_theoretical_yield_button.pack(pady=(10, 15), padx=20)

    def show_theoretical_yield_results_frames(self):
        self.theoretical_yield_results_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=360, height=150)
        self.theoretical_yield_results_frame.grid(row=2, column=1, sticky="w", pady=(10, 10), padx=20)
        self.theoretical_yield_results_frame.grid_propagate(False)

        theoretical_yield_calculation_results_title = ctk.CTkLabel(self.theoretical_yield_results_frame, fg_color="white",
                                                               text="Calculation Results", text_color="black",  font=("Arial", 18),
                                                               anchor="w", justify="left")
        theoretical_yield_calculation_results_title.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=15)

        self.theoretical_yield_calculations_description_frame = ctk.CTkFrame(self.theoretical_yield_results_frame, fg_color=GRAY_COLOUR,
                                                                         corner_radius=15, width=320, height=80)
        self.theoretical_yield_calculations_description_frame.grid(row=1, column=0, sticky="w", pady=(5, 15), padx=20)
        self.theoretical_yield_calculations_description_frame.grid_propagate(False)

        theoretical_yield_analysis_title = ctk.CTkLabel(self.theoretical_yield_calculations_description_frame,
                                                        text="Theoretical Yield Analysis:", text_color="black",
                                                        font=("Arial", 15, "bold"), justify="left")
        theoretical_yield_analysis_title.grid(row=0, pady=(15, 0), padx=20)

        self.theoretical_yield_formula_outer_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=360, height=220)
        self.theoretical_yield_formula_outer_frame.grid(row=3, column=1, sticky="w", pady=(10, 10), padx=20)
        self.theoretical_yield_formula_outer_frame.grid_propagate(False)

        calculation_formula_title = ctk.CTkLabel(self.theoretical_yield_formula_outer_frame, fg_color="white", text="Essential Formula",
                                                 text_color="black", font=("Arial", 18), anchor="w")
        calculation_formula_title.grid(row=0, sticky="w", padx=15, pady=(15, 5))

        theoretical_yield_formula_inner_frame = ctk.CTkFrame(self.theoretical_yield_formula_outer_frame, fg_color=BLUE_COLOUR,
                                                             corner_radius=15, width=330, height=150)
        theoretical_yield_formula_inner_frame.grid(row=1, sticky="w", pady=(5, 15), padx=15)
        theoretical_yield_formula_inner_frame.grid_propagate(False)

        theoretical_yield_calculation_formula_title = ctk.CTkLabel(theoretical_yield_formula_inner_frame, fg_color=BLUE_COLOUR,
                                                                   text="Theoretical Yield", text_color="white",
                                                                   font=("Arial", 14, "bold"), anchor="w")
        theoretical_yield_calculation_formula_title.grid(row=0, column=0, sticky="w", pady=(15, 0), padx=15)

        theoretical_yield_calculation_formula_description = ctk.CTkLabel(theoretical_yield_formula_inner_frame, fg_color=BLUE_COLOUR,
                                                                         text="\nMoles of LR = Mass/Molar Mass of LR\n\n"
                                                                          "Moles of Product = Moles of LR x Stoichiometric Ratio\n\n"
                                                                          "Theoretical Mass = Moles x Molar Mass of Product",
                                                                         text_color="white", font=("Arial", 12), wraplength=330,
                                                                         anchor="w", justify="left")
        theoretical_yield_calculation_formula_description.grid(row=1, column=0, sticky="w", pady=(0, 20), padx=15)

    def check_theoretical_yield_inputs(self):
        try:
            limiting_reagent_mass = float(self.limiting_reagent_mass.get())
            molar_mass_reagent = float(self.molar_mass_reagent.get())
            molar_mass_product = float(self.molar_mass_product.get())
            stoichiometric_ratio = float(self.stoichiometric_ratio.get())

            if molar_mass_reagent < 0 or molar_mass_product < 0 or limiting_reagent_mass < 0 or stoichiometric_ratio < 0:
                self.show_theoretical_yield_error("Mass values and/or stoichiometric ratio must be positive.")
                return

            self.remove_error_message()
            self.calculate_theoretical_yield()
            self.reset_calculate_theoretical_yield_button()
            self.calculate_theoretical_yield_button = ctk.CTkButton(self.theoretical_yield_calculation_frame, width=245,
                                                                    command=self.check_theoretical_yield_inputs,
                                                                    fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                                    text="Calculate", font=("Arial", 10))
            self.calculate_theoretical_yield_button.pack(pady=(10, 15), padx=20)

        except ValueError:
            self.show_theoretical_yield_error("Please enter a valid numeric mass.")

    def calculate_theoretical_yield(self):
        self.reset_theoretical_yield_calculation_frames()
        limiting_reagent_mass = float(self.limiting_reagent_mass.get())
        molar_mass_reagent = float(self.molar_mass_reagent.get())
        molar_mass_product = float(self.molar_mass_product.get())
        stoichiometric_ratio = float(self.stoichiometric_ratio.get())

        theoretical_yield = (limiting_reagent_mass/molar_mass_reagent) * stoichiometric_ratio * molar_mass_product

        self.theoretical_yield_results_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=360, height=150)
        self.theoretical_yield_results_frame.grid(row=2, column=1, sticky="w", pady=(10, 10), padx=20)
        self.theoretical_yield_results_frame.grid_propagate(False)

        theoretical_yield_calculation_results_title = ctk.CTkLabel(self.theoretical_yield_results_frame, fg_color="white",
                                                                   text="Calculation Results", text_color="black", font=("Arial", 18),
                                                                   anchor="w", justify="left")
        theoretical_yield_calculation_results_title.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=15)

        self.theoretical_yield_calculations_description_frame = ctk.CTkFrame(self.theoretical_yield_results_frame, fg_color=GRAY_COLOUR,
                                                                             corner_radius=15, width=320, height=80)
        self.theoretical_yield_calculations_description_frame.grid(row=1, column=0, sticky="w", pady=(5, 15), padx=20)
        self.theoretical_yield_calculations_description_frame.grid_propagate(False)

        theoretical_yield_analysis_title = ctk.CTkLabel(self.theoretical_yield_calculations_description_frame,
                                                        text="Theoretical Yield Analysis:", text_color="black",
                                                        font=("Arial", 15, "bold"), anchor="w", justify="left")
        theoretical_yield_analysis_title.grid(row=0, sticky="w", pady=(10, 0), padx=20)
        theoretical_yield_calculations_description = ctk.CTkLabel(self.theoretical_yield_calculations_description_frame,
                                                                  text=f"The theoretical yield is {theoretical_yield:.2f} grams.",
                                                                  text_color="black", font=("Arial", 11),
                                                                  anchor="w", justify="left")
        theoretical_yield_calculations_description.grid(row=1, pady=(5, 15), padx=20)

    def show_theoretical_yield_error(self, message):
        self.remove_error_message()
        self.reset_calculate_theoretical_yield_button()
        self.calculate_theoretical_yield_button = ctk.CTkButton(self.theoretical_yield_calculation_frame, width=245,
                                                                command=self.check_theoretical_yield_inputs,
                                                                fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                                text="Calculate", font=("Arial", 10))
        self.calculate_theoretical_yield_button.pack(pady=(10, 2), padx=20)
        self.error_label = ctk.CTkLabel(self.theoretical_yield_calculation_frame, fg_color=GRAY_COLOUR,
                                        text=message, text_color="red", font=("Arial", 10, "italic", "bold"))
        self.error_label.pack()

    def reset_calculate_theoretical_yield_button(self):
        if self.calculate_theoretical_yield_button is not None:
            self.calculate_theoretical_yield_button.destroy()
            self.calculate_theoretical_yield_button = None

    def reset_theoretical_yield_calculation_frames(self):
        for widget_name in ["theoretical_yield_results_frame", "theoretical_yield_calculations_description_frame"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def limiting_reagent(self):
        self.limiting_reagent_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=320, height=420)
        self.limiting_reagent_frame.grid(row=2, column=0, rowspan=2, sticky="w", pady=(10, 10), padx=20)
        self.limiting_reagent_frame.grid_propagate(False)

        limiting_reagent_calculator_title = ctk.CTkLabel(self.limiting_reagent_frame, fg_color="white",
                                                         text="Limiting Reagent Calculator", text_color="black",
                                                         font=("Arial", 18), anchor="w")
        limiting_reagent_calculator_title.grid(row=0, column=0, sticky="w", pady=(15, 3), padx=15)

        limiting_reagent_description_frame = ctk.CTkFrame(self.limiting_reagent_frame, fg_color=BLUE_COLOUR, corner_radius=15)
        limiting_reagent_description_frame.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=20)

        limiting_reagent_calculator_description = ctk.CTkLabel(limiting_reagent_description_frame, fg_color=BLUE_COLOUR,
                                                                    text="Identify the limiting reagent in your reaction. "
                                                                         "This is the reactant that runs out first and determines "
                                                                         "the maximum amount of product that can be formed, "
                                                                         "impacting your overall reaction yield.",
                                                                    text_color="white", font=("Arial", 11),
                                                                    wraplength=260, justify="left")
        limiting_reagent_calculator_description.pack(pady=(15, 15), padx=(15, 8))

        self.limiting_reagent_calculation_frame = ctk.CTkFrame(self.limiting_reagent_frame, fg_color=GRAY_COLOUR, corner_radius=15)
        self.limiting_reagent_calculation_frame.grid(row=2, column=0, sticky="w", pady=(10, 3), padx=15)


        self.reagent1_mass = ctk.CTkEntry(self.limiting_reagent_calculation_frame, width=245, height=25, corner_radius=8,
                                          fg_color="white", placeholder_text="Reagent 1 mass (g)", placeholder_text_color=DARK_GRAY_COLOUR,
                                          text_color="black", font=("Arial", 10), justify = "left")
        self.reagent1_mass.pack(pady=(10, 5), padx=(15, 15))

        self.reagent1_molar_mass = ctk.CTkEntry(self.limiting_reagent_calculation_frame, width=245, height=25, corner_radius=8,
                                                fg_color="white", placeholder_text="Reagent 1 molar mass (g/mol)",
                                                placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                                font=("Arial", 10), justify="left")
        self.reagent1_molar_mass.pack(pady=(5, 10), padx=(15, 15))

        self.reagent2_mass = ctk.CTkEntry(self.limiting_reagent_calculation_frame, width=245, height=25, corner_radius=8,
                                          fg_color="white", placeholder_text="Reagent 2 mass (g)",
                                          placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                          font=("Arial", 10), justify="left")
        self.reagent2_mass.pack(pady=(5, 5), padx=(15, 15))

        self.reagent2_molar_mass = ctk.CTkEntry(self.limiting_reagent_calculation_frame, width=245, height=25, corner_radius=8,
                                                fg_color="white", placeholder_text="Reagent 2 molar mass (g/mol)",
                                                placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                                font=("Arial", 10), justify="left")
        self.reagent2_molar_mass.pack(pady=(5, 10), padx=(15, 15))

        self.reagents_stoichiometric_ratio = ctk.CTkEntry(self.limiting_reagent_calculation_frame, width=245, height=25,
                                                          corner_radius=8, fg_color="white",
                                                          placeholder_text="Stoichiometric Ratio (1:n)",
                                                          placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                                          font=("Arial", 10), justify="left")
        self.reagents_stoichiometric_ratio.pack(pady=(5, 10), padx=(15, 15))

        self.calculate_limiting_reagent_button = ctk.CTkButton(self.limiting_reagent_calculation_frame, width=245,
                                                          command=self.check_limiting_reagent_inputs,fg_color=BLUE_COLOUR,
                                                          hover_color=DARK_BLUE_COLOUR, text="Calculate", font=("Arial", 10))
        self.calculate_limiting_reagent_button.pack(pady=(5, 15), padx=(15, 15))

    def show_limiting_reagent_results_frames(self):
        self.limiting_reagent_results_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=360, height=150)
        self.limiting_reagent_results_frame.grid(row=2, column=1, sticky="w", pady=(10, 10), padx=20)
        self.limiting_reagent_results_frame.grid_propagate(False)

        limiting_reagent_calculation_results_title = ctk.CTkLabel(self.limiting_reagent_results_frame, fg_color="white",
                                                               text="Calculation Results", text_color="black", font=("Arial", 18),
                                                               anchor="w", justify="left")
        limiting_reagent_calculation_results_title.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=15)

        self.limiting_reagent_calculations_description_frame = ctk.CTkFrame(self.limiting_reagent_results_frame,
                                                                         fg_color=GRAY_COLOUR, corner_radius=15, width=320, height=80)
        self.limiting_reagent_calculations_description_frame.grid(row=1, column=0, sticky="w", pady=(5, 15), padx=20)
        self.limiting_reagent_calculations_description_frame.grid_propagate(False)

        limiting_reagent_analysis_title = ctk.CTkLabel(self.limiting_reagent_calculations_description_frame,
                                                       text="Limiting Reagent Analysis:", text_color="black",
                                                       font=("Arial", 15, "bold"), justify="left")
        limiting_reagent_analysis_title.grid(row=0, pady=(15, 0), padx=20)

        self.limiting_reagent_formula_outer_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15,
                                                              width=360, height=220)
        self.limiting_reagent_formula_outer_frame.grid(row=3, column=1, sticky="w", pady=(10, 10), padx=20)
        self.limiting_reagent_formula_outer_frame.grid_propagate(False)

        calculation_formula_title = ctk.CTkLabel(self.limiting_reagent_formula_outer_frame, text="Essential Formula",
                                                 text_color="black", fg_color="white", font=("Arial", 18), anchor="w")
        calculation_formula_title.grid(row=0, sticky="w", pady=(15, 5), padx=15)

        limiting_reagent_formula_inner_frame = ctk.CTkFrame(self.limiting_reagent_formula_outer_frame,
                                                            fg_color=BLUE_COLOUR, corner_radius=15, width=330, height=150)
        limiting_reagent_formula_inner_frame.grid(row=1, sticky="w", pady=(5, 15), padx=15)
        limiting_reagent_formula_inner_frame.grid_propagate(False)

        limiting_reagent_calculation_formula_title = ctk.CTkLabel(limiting_reagent_formula_inner_frame, fg_color=BLUE_COLOUR,
                                                               text="Finding Limiting Reagent", text_color="white",
                                                               font=("Arial", 14, "bold"), anchor="w")
        limiting_reagent_calculation_formula_title.grid(row=0, column=0, sticky="w", pady=(15, 0), padx=15)

        limiting_reagent_calculation_formula_description = ctk.CTkLabel(limiting_reagent_formula_inner_frame, fg_color=BLUE_COLOUR,
                                                                        text="\nMoles of Reagent 1 = Mass/Molar Mass of Reagent 1\n\n"
                                                                          "Moles of Reagent 2 = Mass/Molar Mass of Reagent 2\n\n"
                                                                          "Compare moles and whichever is smaller is the LR",
                                                                        text_color="white", font=("Arial", 12), wraplength=330,
                                                                        anchor="w", justify="left")
        limiting_reagent_calculation_formula_description.grid(row=1, column=0, sticky="w", pady=(0, 20), padx=15)

    def check_limiting_reagent_inputs(self):
        try:
            reagent1_mass = float(self.reagent1_mass.get())
            reagent1_molar_mass = float(self.reagent1_molar_mass.get())
            reagent2_mass = float(self.reagent2_mass.get())
            reagent2_molar_mass = float(self.reagent2_molar_mass.get())
            reagents_stoichiometric_ratio = float(self.reagents_stoichiometric_ratio.get())

            if reagent1_mass < 0 or reagent2_mass < 0 or reagent1_molar_mass < 0 or reagent2_molar_mass < 0 or reagents_stoichiometric_ratio < 0:
                self.show_limiting_reagent_error("Mass values and/or stoichiometric ratio must be positive.")
                return

            self.remove_error_message()
            self.calculate_limiting_reagent()
            self.reset_calculate_limiting_reagent_button()
            self.calculate_limiting_reagent_button = ctk.CTkButton(self.limiting_reagent_calculation_frame, width=245,
                                                                   command=self.check_limiting_reagent_inputs,
                                                                   fg_color=BLUE_COLOUR,
                                                                   hover_color=DARK_BLUE_COLOUR, text="Calculate",
                                                                   font=("Arial", 10))
            self.calculate_limiting_reagent_button.pack(pady=(5, 15), padx=(15, 15))

        except ValueError:
            self.show_limiting_reagent_error("Please enter a valid numeric mass.")

    def calculate_limiting_reagent(self):
        self.reset_limiting_reagent_calculation_frames()
        reagent1_mass = float(self.reagent1_mass.get())
        reagent1_molar_mass = float(self.reagent1_molar_mass.get())
        reagent2_mass = float(self.reagent2_mass.get())
        reagent2_molar_mass = float(self.reagent2_molar_mass.get())
        reagents_stoichiometric_ratio = float(self.reagents_stoichiometric_ratio.get())

        reagent1_moles = reagent1_mass / reagent1_molar_mass
        reagent2_moles = reagent2_mass / reagent2_molar_mass
        reagent2_moles_with_ratio = reagent2_moles / reagents_stoichiometric_ratio

        if reagent1_moles > reagent2_moles_with_ratio:
            limiting_reagent_results_text = ["Reagent 2 is the limiting reagent while reagent 1 is in excess."]

        elif reagent1_moles < reagent2_moles_with_ratio:
            limiting_reagent_results_text = ["Reagent 1 is the limiting reagent while reagent 2 is in excess."]

        elif reagent1_moles == reagent2_moles_with_ratio:
            limiting_reagent_results_text = ["There is no limiting reagent in the reaction."]

        limiting_reagent_results_text.append(f"Moles of Reagent 1: {reagent1_moles:.2f}")
        limiting_reagent_results_text.append(f"Moles of Reagent 2: {reagent2_moles:.2f}")

        limiting_reagent_results_text = "\n".join(limiting_reagent_results_text)


        self.limiting_reagent_results_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=360, height=150)
        self.limiting_reagent_results_frame.grid(row=2, column=1, sticky="w", pady=(10, 10), padx=20)
        self.limiting_reagent_results_frame.grid_propagate(False)

        limiting_reagent_calculation_results_title = ctk.CTkLabel(self.limiting_reagent_results_frame, fg_color="white",
                                                                   text="Calculation Results", text_color="black",
                                                                   font=("Arial", 18), anchor="w", justify="left")
        limiting_reagent_calculation_results_title.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=15)

        self.limiting_reagent_calculations_description_frame = ctk.CTkFrame(self.limiting_reagent_results_frame,
                                                                            fg_color=GRAY_COLOUR, corner_radius=15, width=320, height=80)
        self.limiting_reagent_calculations_description_frame.grid(row=1, column=0, sticky="w", pady=(5, 15), padx=20)
        self.limiting_reagent_calculations_description_frame.grid_propagate(False)

        limiting_reagent_analysis_title = ctk.CTkLabel(self.limiting_reagent_calculations_description_frame,
                                                        text="Limiting Reagent Analysis:", text_color="black",
                                                       font=("Arial", 15, "bold"), anchor="w", justify="left",)
        limiting_reagent_analysis_title.grid(row=0, sticky="w", pady=(10, 0), padx=20)
        limiting_reagent_calculations_description = ctk.CTkLabel(self.limiting_reagent_calculations_description_frame,
                                                                  text=limiting_reagent_results_text, text_color="black",
                                                                 font=("Arial", 11), anchor="w", justify="left")
        limiting_reagent_calculations_description.grid(row=1, pady=(5, 15), padx=20)

    def show_limiting_reagent_error(self, message):
        self.remove_error_message()
        self.reset_calculate_limiting_reagent_button()
        self.calculate_limiting_reagent_button = ctk.CTkButton(self.limiting_reagent_calculation_frame, width=245,
                                                               command=self.check_limiting_reagent_inputs,
                                                               fg_color=BLUE_COLOUR,
                                                               hover_color=DARK_BLUE_COLOUR, text="Calculate",
                                                               font=("Arial", 10))
        self.calculate_limiting_reagent_button.pack(pady=(5, 2), padx=(15, 15))
        self.error_label = ctk.CTkLabel(self.limiting_reagent_calculation_frame, text=message, text_color="red",
                                        fg_color=GRAY_COLOUR, font=("Arial", 10, "italic", "bold"))
        self.error_label.pack()

    def reset_calculate_limiting_reagent_button(self):
        if self.calculate_limiting_reagent_button is not None:
            self.calculate_limiting_reagent_button.destroy()
            self.calculate_limiting_reagent_button = None

    def reset_limiting_reagent_calculation_frames(self):
        for widget_name in ["limiting_reagent_results_frame", "limiting_reagent_calculations_description_frame"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def show_general_information(self):
        self.information_frame = ctk.CTkFrame(self.window, fg_color="#d2d2d2", corner_radius=15)
        self.information_frame.grid(row=0, column=2, rowspan=4, sticky="ew", pady=(10, 10), padx=20)

        concept_of_yield_outer_frame = ctk.CTkFrame(self.information_frame, fg_color="white", corner_radius=15, width=455, height=170)
        concept_of_yield_outer_frame.grid(row=0, sticky="w", pady=(10, 5), padx=15)
        concept_of_yield_outer_frame.grid_propagate(False)

        concept_of_yield_inner_frame = ctk.CTkFrame(concept_of_yield_outer_frame, fg_color=BLUE_COLOUR, corner_radius=15, width=425, height=150)
        concept_of_yield_inner_frame.grid(row=0, sticky="w", pady=(10, 10), padx=15)
        concept_of_yield_inner_frame.grid_propagate(False)

        basic_concepts_title = ctk.CTkLabel(concept_of_yield_inner_frame, fg_color=BLUE_COLOUR, text="Basic Concepts of Chemical Yield",
                                            text_color="white", font=("Arial", 16, "bold"), anchor="w")
        basic_concepts_title.grid(row=0, column=0, sticky="w", pady=(15, 0), padx=15)

        basic_concepts_description = ctk.CTkLabel(concept_of_yield_inner_frame, fg_color=BLUE_COLOUR,
                                                  text="• Actual Yield: This is the amount of product you actually collect.\n"
                                                       "• Theoretical Yield: This is the maximum amount of product that could be formed.\n"
                                                       "• Percent Yield: This tells you how efficient your reaction was.\n"
                                                       "• Limiting Reagent: The reactant in the reaction that will run out before the others.\n",
                                                  text_color="white", font=("Arial", 12), wraplength=400,
                                                  anchor="w", justify="left")
        basic_concepts_description.grid(row=1, column=0, sticky="w", pady=(5, 10), padx=15)

        factors_affecting_yield_outer_frame = ctk.CTkFrame(self.information_frame, fg_color="white", corner_radius=15, width=455, height=160)
        factors_affecting_yield_outer_frame.grid(row=1, sticky="w", pady=(5, 5), padx=15)
        factors_affecting_yield_outer_frame.grid_propagate(False)

        factors_affecting_yield_inner_frame = ctk.CTkFrame(factors_affecting_yield_outer_frame, fg_color=GRAY_COLOUR, corner_radius=15, width=425, height=140)
        factors_affecting_yield_inner_frame.grid(row=0, sticky="w", pady=(10, 15), padx=15)
        factors_affecting_yield_inner_frame.grid_propagate(False)

        factors_yield_title = ctk.CTkLabel(factors_affecting_yield_inner_frame, fg_color=GRAY_COLOUR,
                                           text="Factors Affecting Reaction Yield", text_color="black",
                                           font=("Arial", 16, "bold"), anchor="w")
        factors_yield_title.grid(row=0, column=0, sticky="w", pady=(15, 0), padx=15)

        factors_yield_description = ctk.CTkLabel(factors_affecting_yield_inner_frame, fg_color=GRAY_COLOUR,
                                                  text="1. Side Reactions\n"
                                                       "2. Incomplete Reactions\n"
                                                       "3. Product Loss\n"
                                                       "4. Reaction Conditions\n"
                                                       "5. Equilibrium Limitations\n",
                                                  text_color="black", font=("Arial", 12), wraplength=400,
                                                   anchor="w", justify="left")
        factors_yield_description.grid(row=1, column=0, sticky="w", pady=(5, 10), padx=15)

        types_of_yield_outer_frame = ctk.CTkFrame(self.information_frame, fg_color="white", corner_radius=15, width=455, height=190)
        types_of_yield_outer_frame.grid(row=2, sticky="w", pady=(5, 5), padx=15)
        types_of_yield_outer_frame.grid_propagate(False)

        types_of_yield_inner_frame = ctk.CTkFrame(types_of_yield_outer_frame, fg_color=BLUE_COLOUR, corner_radius=15, width=425, height=170)
        types_of_yield_inner_frame.grid(row=0, sticky="w", pady=(10, 15), padx=15)
        types_of_yield_inner_frame.grid_propagate(False)

        factors_yield_title = ctk.CTkLabel(types_of_yield_inner_frame, fg_color=BLUE_COLOUR, text="Different Types of Yields",
                                           text_color="white", font=("Arial", 16, "bold"), anchor="w")
        factors_yield_title.grid(row=0, column=0, sticky="w", pady=(15, 0), padx=15)

        factors_yield_description = ctk.CTkLabel(types_of_yield_inner_frame, fg_color=BLUE_COLOUR,
                                                  text="• Chemical Yield: The general term for the amount of product obtained from a chemical reaction.\n"
                                                       "• Isolated Yield: The amount of purified product obtained after all separation and purification steps.\n"
                                                       "• Crude Yield: The amount of product obtained before any purification.\n"
                                                       "• Overall Yield: In multi-step reactions, this is the total yield from start to finish.\n",
                                                  text_color="white", font=("Arial", 12), wraplength=400,
                                                  anchor="w", justify="left")
        factors_yield_description.grid(row=1, column=0, sticky="w", pady=(5, 10), padx=15)

    def remove_dropdown_menu(self):
        if self.dropdown_menu_frame is not None:
            self.dropdown_menu_frame.destroy()
            setattr(self, "dropdown_menu_frame", None)

    def remove_yield_frames(self):
        for widget_name in ["percent_yield_frame", "percent_yield_formula_outer_frame", "percent_yield_results_frame",
                            "theoretical_yield_frame", "theoretical_yield_formula_outer_frame", "theoretical_yield_results_frame",
                            "limiting_reagent_frame", "limiting_reagent_formula_outer_frame", "limiting_reagent_results_frame", "information_frame"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def ask_reagent_count(self):
        self.number_of_reagents_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=500, height=130)
        self.number_of_reagents_frame.grid(row=2, column=0, sticky="w", pady=(10, 10), padx=20)
        self.number_of_reagents_frame.grid_propagate(False)

        number_of_reagents_title = ctk.CTkLabel(self.number_of_reagents_frame, fg_color="white",
                                                text="Enter the number of reagents...", text_color="black",
                                                font=("Arial", 14), anchor="w")
        number_of_reagents_title.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=15)

        number_of_reagents_input_frame = ctk.CTkFrame(self.number_of_reagents_frame, fg_color=GRAY_COLOUR, corner_radius=15)
        number_of_reagents_input_frame.grid(row=1, column=0, sticky="w", pady=(0, 10), padx=20)

        number_of_reagents_input = ctk.CTkEntry(number_of_reagents_input_frame, width=360, fg_color="white",
                                                text_color="black", textvariable=self.number_reagents, justify="center")
        number_of_reagents_input.grid(row=1, column=0, sticky="w", pady=(15, 15), padx=(15, 5))

        decrease_reagent_count_button = ctk.CTkButton(number_of_reagents_input_frame,width=30, command=self.decrease_reagent_count,
                                                      fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                      text="-", text_color="white", font=("Arial", 10, "bold"))
        decrease_reagent_count_button.grid(row=1, column=1, sticky="w", pady=(15, 15), padx=(0,5))
        increase_reagent_count_button = ctk.CTkButton(number_of_reagents_input_frame, width=30, command=self.increase_reagent_count,
                                                      fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR,
                                                      text="+", text_color="white", font=("Arial", 10, "bold"))
        increase_reagent_count_button.grid(row=1, column=2, sticky="w", pady=(15, 15), padx=(0, 15))

        self.types_of_reagents_outer_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=500, height=270)
        self.types_of_reagents_outer_frame.grid(row=3, column=0, sticky="w", pady=(10, 10), padx=20)
        self.types_of_reagents_outer_frame.grid_propagate(False)

        self.types_of_reagents_inner_frame = ctk.CTkFrame(self.types_of_reagents_outer_frame, fg_color=GRAY_COLOUR,
                                                          corner_radius=15, width=455, height=230)
        self.types_of_reagents_inner_frame.grid(row=4, column=0, sticky="w", pady=(20, 15), padx=20)
        self.types_of_reagents_inner_frame.grid_propagate(False)

        self.buttons_frame = ctk.CTkFrame(self.window, fg_color=BACKGROUND_COLOUR, corner_radius=15)
        self.buttons_frame.grid(row=4, column=0, sticky="w", pady=(0, 10), padx=20)

        submit_inputs_button = ctk.CTkButton(self.buttons_frame, command=self.submit_inputs, fg_color=BLUE_COLOUR,
                                      hover_color=DARK_BLUE_COLOUR, text="Submit", font=("Arial", 10))
        submit_inputs_button.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=35)
        reset_detailed_option_button = ctk.CTkButton(self.buttons_frame, command=self.reset_detailed_options, fg_color=BLUE_COLOUR,text="Reset",
                                            hover_color=DARK_BLUE_COLOUR, font=("Arial", 10))
        reset_detailed_option_button.grid(row=0, column=1, sticky="w", pady=(10, 10), padx=(100, 20))

    def increase_reagent_count(self):
        number_of_reagents = int(self.number_reagents.get())
        if number_of_reagents < 4:
            self.number_reagents.set(str(number_of_reagents + 1))
            self.update_reagent_entries()

    def decrease_reagent_count(self):
        number_of_reagents = int(self.number_reagents.get())
        if number_of_reagents > 0:
            self.number_reagents.set(str(number_of_reagents - 1))
            self.update_reagent_entries()

    def update_reagent_entries(self):
        for widget in self.types_of_reagents_inner_frame.winfo_children():
            widget.destroy()
        self.reagent_stoichiometry_entries.clear()
        self.reagent_formula_entries.clear()
        self.reagent_mass_entries.clear()

        count = int(self.number_reagents.get())
        for i in range(count):
            pady_rule = (15, 10) if i == 0 else (10, 10)

            reagent_label = ctk.CTkLabel(self.types_of_reagents_inner_frame, fg_color=GRAY_COLOUR,
                                         text=f"Reagent {i + 1}:", text_color=BLUE_COLOUR,
                                         font=("Arial", 13, "bold"), anchor="w")
            reagent_label.grid(row=i, column=0, pady=pady_rule, padx=15)

            reagent_stoichiometry_input = ctk.CTkEntry(self.types_of_reagents_inner_frame, width=80, height=25, corner_radius=8,
                                                       fg_color="white", placeholder_text="Coefficient",
                                                       placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                                       font=("Arial", 10), justify="left")
            reagent_stoichiometry_input.grid(row=i, column=1, pady=pady_rule, padx=5)

            reagent_formula_input = ctk.CTkEntry(self.types_of_reagents_inner_frame, width=150, height=25, corner_radius=8,
                                                 fg_color="white", placeholder_text="Chemical Formula",
                                                 placeholder_text_color=DARK_GRAY_COLOUR,  text_color="black",
                                                 font=("Arial", 10), justify="left")
            reagent_formula_input.grid(row=i, column=2, pady=pady_rule, padx=5)

            reagent_mass_input = ctk.CTkEntry(self.types_of_reagents_inner_frame, width=80, height=25, corner_radius=8,
                                              fg_color="white", placeholder_text="Mass (g)",
                                              placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                              font=("Arial", 10), justify="left")
            reagent_mass_input.grid(row=i, column=3, pady=pady_rule, padx=(5, 15))

            self.reagent_stoichiometry_entries.append(reagent_stoichiometry_input)
            self.reagent_formula_entries.append(reagent_formula_input)
            self.reagent_mass_entries.append(reagent_mass_input)

    def ask_product_count(self):
        self.number_of_products_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=590, height=130)
        self.number_of_products_frame.grid(row=2, column=1, sticky="w", pady=(10, 10), padx=20)
        self.number_of_products_frame.grid_propagate(False)

        number_of_products_title = ctk.CTkLabel(self.number_of_products_frame, fg_color="white",
                                                text="Enter the number of products...", text_color="black",
                                                font=("Arial", 14), anchor="w")
        number_of_products_title.grid(row=0, column=0, sticky="w", pady=(15, 3), padx=15)

        number_of_products_input_frame = ctk.CTkFrame(self.number_of_products_frame, fg_color=GRAY_COLOUR, corner_radius=15)
        number_of_products_input_frame.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=20)

        number_of_products_input = ctk.CTkEntry(number_of_products_input_frame,  width=450, fg_color="white", text_color="black",
                                                textvariable=self.number_products, justify="center")
        number_of_products_input.grid(row=1, column=0, sticky="w", pady=(15, 15), padx=(15, 5))

        decrease_product_count_button = ctk.CTkButton(number_of_products_input_frame, width=30, command=self.decrease_product_count,
                                                      fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR, text="-",
                                                      text_color="white", font=("Arial", 10, "bold"))
        decrease_product_count_button.grid(row=1, column=1, sticky="w", pady=(15, 15), padx=(0,5))
        increase_product_count_button = ctk.CTkButton(number_of_products_input_frame, width=30, command=self.increase_product_count,
                                                      fg_color=BLUE_COLOUR, hover_color=DARK_BLUE_COLOUR, text="+",
                                                      text_color="white", font=("Arial", 10, "bold"))
        increase_product_count_button.grid(row=1, column=2, sticky="w", pady=(15, 15), padx=(0, 15))

        self.types_of_products_outer_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=590, height=270)
        self.types_of_products_outer_frame.grid(row=3, column=1, sticky="w", pady=(10, 10), padx=20)
        self.types_of_products_outer_frame.grid_propagate(False)

        self.types_of_products_inner_frame = ctk.CTkFrame(self.types_of_products_outer_frame, fg_color=GRAY_COLOUR,
                                                          corner_radius=15, width=550, height=230)
        self.types_of_products_inner_frame.grid(row=4, column=0, sticky="w", pady=(20, 15), padx=20)
        self.types_of_products_inner_frame.grid_propagate(False)

        self.errors_frame = ctk.CTkFrame(self.window, fg_color=BACKGROUND_COLOUR, corner_radius=15, width=590, height=50)
        self.errors_frame.grid(row=4, column=1, sticky="w", pady=(0, 10), padx=20)
        self.errors_frame.grid_propagate(False)

    def increase_product_count(self):
        number_of_products = int(self.number_products.get())
        if number_of_products < 4:
            self.number_products.set(str(number_of_products + 1))
            self.update_product_entries()

    def decrease_product_count(self):
        number_of_products = int(self.number_products.get())
        if number_of_products > 0:
            self.number_products.set(str(number_of_products - 1))
            self.update_product_entries()

    def update_product_entries(self):
        for widget in self.types_of_products_inner_frame.winfo_children():
            widget.destroy()
        self.product_stoichiometry_entries.clear()
        self.product_formula_entries.clear()
        self.product_mass_entries.clear()

        count = int(self.number_products.get())
        for i in range(count):
            pady_rule = (15, 10) if i == 0 else (10, 10)

            product_label = ctk.CTkLabel(self.types_of_products_inner_frame, fg_color=GRAY_COLOUR, text=f"Product {i + 1}:",
                                         text_color=BLUE_COLOUR, font=("Arial", 13, "bold"), anchor="w")
            product_label.grid(row=i, column=0, pady=pady_rule, padx=15)

            product_stoichiometry_input = ctk.CTkEntry(self.types_of_products_inner_frame, width=80, height=25, corner_radius=8,
                                                       fg_color="white", placeholder_text="Coefficient",
                                                       placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                                       font=("Arial", 10), justify="left")
            product_stoichiometry_input.grid(row=i, column=1, pady=pady_rule, padx=5)

            product_formula_input = ctk.CTkEntry(self.types_of_products_inner_frame, width=150, height=25, corner_radius=8,
                                                 fg_color="white", placeholder_text="Chemical Formula",
                                                 placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                                 font=("Arial", 10), justify="left")
            product_formula_input.grid(row=i, column=2, pady=pady_rule, padx=5)

            product_mass_input = ctk.CTkEntry(self.types_of_products_inner_frame, width=85, height=25, corner_radius=8,
                                              fg_color="white", placeholder_text="Actual Mass (g)",
                                              placeholder_text_color=DARK_GRAY_COLOUR, text_color="black",
                                              font=("Arial", 10), justify="left")
            product_mass_input.grid(row=i, column=3, pady=pady_rule, padx=5)

            choose_main_product_radiobutton = ctk.CTkRadioButton(self.types_of_products_inner_frame, fg_color=BLUE_COLOUR,
                                                                 hover_color=DARK_BLUE_COLOUR, text="Main Product",
                                                                 text_color="black",  font=("Arial", 10),
                                                                 variable=self.main_product, value=i)
            choose_main_product_radiobutton.grid(row=i, column=4, pady=pady_rule, padx=(5, 15))

            self.product_stoichiometry_entries.append(product_stoichiometry_input)
            self.product_formula_entries.append(product_formula_input)
            self.product_mass_entries.append(product_mass_input)

        def submit(self):
            self.append_dictionaries()
            if not self.reagents:
                return
            if not self.products:
                return

            self.calculate_reagent_mole_ratios()
            self.determine_limiting_reagent()
            self.calculate_main_product_moles()
            self.remove_reagent_product_frames()
            self.window.state("zoomed")
            self.show_equation()
            self.show_reagent_moles()
            self.show_product_moles()
            self.show_percentage_yield()
            self.show_detailed_general_information()

    def submit_inputs(self):
        self.reagents = []
        self.products = []

        for s, f, m in zip(self.reagent_stoichiometry_entries,
                           self.reagent_formula_entries,
                           self.reagent_mass_entries):
            self.reagents.append({
                "stoichiometric": s.get(),
                "formula": f.get(),
                "mass": m.get()
            })

        for s, f, m in zip(self.product_stoichiometry_entries,
                           self.product_formula_entries,
                           self.product_mass_entries):
            self.products.append({
                "stoichiometric": s.get(),
                "formula": f.get(),
                "mass": m.get()
            })

        if not self.check_reagent_inputs():
            return
        if not self.check_product_inputs():
            return

        try:
            self.calculate_reagent_mole_ratios()
            self.determine_limiting_reagent()
            self.calculate_main_product_moles()

            self.remove_reagent_product_frames()
            self.window.state("zoomed")
            self.show_equation()
            self.show_reagent_moles()
            self.show_product_moles()
            self.show_percentage_yield()
            self.show_detailed_general_information()

        except Exception as e:
            self.show_reagent_input_error(f"Unexpected error: {e}")
            return

    def check_reagent_inputs(self):
        try:
            valid_reagents = []
            for reagent in self.reagents:
                coefficient = float(reagent["stoichiometric"])
                mass = float(reagent["mass"])

                if coefficient <= 0:
                    raise ValueError("Stoichiometric coefficient must be > 0")
                if mass < 0:
                    raise ValueError("Mass cannot be negative")

                molar_mass = self.calculate_molar_mass(reagent["formula"])

                valid_reagents.append({
                    "stoichiometric": coefficient,
                    "formula": reagent["formula"],
                    "mass": mass,
                    "molar mass": molar_mass,
                })

            self.reagents = valid_reagents
            self.remove_error_message()
            return True

        except ValueError as e:
            self.show_reagent_input_error(f"Error while calculating molar mass: {e}")
            return False

        except Exception as e:
            self.show_reagent_input_error(f"Invalid reagent input, {e}")
            return False

    def show_reagent_input_error(self, message):
        if hasattr(self, "reagents_error_label") and self.reagents_error_label:
            self.reagents_error_label.destroy()

        self.reagents_error_label = ctk.CTkLabel(self.errors_frame, fg_color=BACKGROUND_COLOUR, text=message,
                                                 text_color="red", font=("Arial", 12, "italic", "bold"))
        self.reagents_error_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)

    def check_product_inputs(self):
        try:
            valid_products = []
            for product in self.products:
                coefficient = float(product["stoichiometric"])
                mass = float(product["mass"])

                if coefficient <= 0:
                    raise ValueError("Stoichiometric coefficient must be > 0")
                if mass < 0:
                    raise ValueError("Mass cannot be negative")

                molar_mass = self.calculate_molar_mass(product["formula"])

                valid_products.append({
                    "stoichiometric": coefficient,
                    "formula": product["formula"],
                    "mass": mass,
                    "molar mass": molar_mass,
                })

            self.products = valid_products
            self.remove_error_message()
            return True

        except ValueError as e:
            self.show_product_input_error(f"Error while calculating molar mass: {e}")
            return False

        except Exception as e:
            self.show_product_input_error(f"Invalid reagent input, {e}")
            return False

    def show_product_input_error(self, message):
        if hasattr(self, "products_error_label") and self.products_error_label:
            self.products_error_label.destroy()

        self.products_error_label = ctk.CTkLabel(self.errors_frame, fg_color=BACKGROUND_COLOUR, text=message,
                                                 text_color="red", font=("Arial", 12, "italic", "bold"))
        self.products_error_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)

    def calculate_molar_mass(self, molecular_formula):
        molecular_formula = re.sub(r'[\+\-]\d*', '', molecular_formula)
        hydrate_parts = molecular_formula.split("·")

        total_mass = 0.0
        for part in hydrate_parts:
            tokens = re.findall(r"([A-Z][a-z]?|\d+|\(|\)|\[|\])", part)
            stack = [[]]
            i = 0

            while i < len(tokens):
                token = tokens[i]

                if token in ("(", "["):
                    stack.append([])

                elif token in (")", "]"):
                    group_mass = sum(stack.pop())
                    multiplier = 1
                    if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                        multiplier = int(tokens[i + 1])
                        i += 1
                    stack[-1].append(group_mass * multiplier)

                elif token.isdigit():
                    stack[-1][-1] *= int(token)

                else:
                    if token not in ELEMENTS:
                        raise ValueError(f"Unknown element: {token}")
                    stack[-1].append(ELEMENTS[token])

                i += 1

            total_mass += sum(stack.pop())

        return total_mass

    def calculate_reagent_mole_ratios(self):
        for reagent in self.reagents:
            if reagent.get("error"):
                continue

        for reagent in self.reagents:
            mass = float(reagent["mass"])
            molar_mass_reagents = self.calculate_molar_mass(reagent["formula"])
            moles_reagents = mass / molar_mass_reagents if molar_mass_reagents > 0 else 0
            coefficient = float(reagent["stoichiometric"])
            ratio_reagents = moles_reagents / coefficient

            reagent["molar mass"] = molar_mass_reagents
            reagent["moles"] = moles_reagents
            reagent["ratio"] = ratio_reagents

    def determine_limiting_reagent(self):
        limiting = None
        smallest_ratio = float("inf")

        for reagent in self.reagents:
            ratio = reagent.get("ratio")

            if ratio < smallest_ratio:
                smallest_ratio = ratio
                limiting = reagent

        return limiting

    def calculate_main_product_moles(self):
        if not self.products or self.main_product.get() >= len(self.products):
            return

        limiting_reagent = self.determine_limiting_reagent()
        limiting_stoichiometry = float(limiting_reagent['stoichiometric']) if limiting_reagent['stoichiometric'] else 1.0
        limiting_moles = float(limiting_reagent['moles'])

        selected_index = self.main_product.get()
        main_product = self.products[selected_index]
        main_product_molar_mass = self.calculate_molar_mass(main_product["formula"])
        main_product_stoichiometry = float(main_product["stoichiometric"]) if main_product["stoichiometric"] else 1.0

        main_product_moles = limiting_moles / limiting_stoichiometry * main_product_stoichiometry
        main_product_theoretical_mass = main_product_moles * main_product_molar_mass
        main_product_actual_mass = float(main_product["mass"]) if main_product["mass"] else 0.0
        if main_product_theoretical_mass == 0:
            self.show_product_input_error("Theoretical mass is zero – check inputs.")
            return

        main_product_percent_yield = main_product_actual_mass / main_product_theoretical_mass * 100

        main_product["molar mass"] = main_product_molar_mass
        main_product["moles"] = main_product_moles
        main_product["actual mass"] = main_product_actual_mass
        main_product["theoretical mass"] = main_product_theoretical_mass
        main_product["percent yield"] = main_product_percent_yield

    def format_coefficient(self, value):
        try:
            value = float(value)
            if value == 1:
                return ""

            if value.is_integer():
                return str(int(value))
            return str(value)
        except:
            return ""

    def show_equation(self):
        reagent_side = " + ".join(f"{self.format_coefficient(reagent['stoichiometric'])} {reagent['formula']}".strip()
                                    for reagent in self.reagents)
        product_side = " + ".join(f"{self.format_coefficient(product['stoichiometric'])} {product['formula']}".strip()
                                    for product in self.products)
        equation = f"{reagent_side} → {product_side}"

        self.equation_outer_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=860, height=70)
        self.equation_outer_frame.grid(row=2, columnspan=2, sticky="ew", pady=(10, 10), padx=(20, 10))
        self.equation_outer_frame.grid_propagate(False)

        equation_inner_frame = ctk.CTkFrame(self.equation_outer_frame, fg_color=BLUE_COLOUR, corner_radius=15,  width=700, height=50)
        equation_inner_frame.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=10)
        equation_inner_frame.grid_propagate(False)

        full_equation_title = ctk.CTkLabel(equation_inner_frame, fg_color=BLUE_COLOUR, text="Equation:", text_color="white",
                                           font=("Arial", 16, "bold"), anchor="w")
        full_equation_title.grid(row=0, column=0, sticky="w", pady=(10, 15), padx=(15, 5))

        full_equation = ctk.CTkLabel(equation_inner_frame, fg_color=BLUE_COLOUR, text=equation, text_color="white",
                                     font=("Arial", 16), anchor="w")
        full_equation.grid(row=0, column=1, sticky="w", pady=(10, 15), padx=5)

        reset_button_frame = ctk.CTkFrame(self.equation_outer_frame, fg_color=GRAY_COLOUR, corner_radius=15, width=110, height=50)
        reset_button_frame.grid(row=0, column=1, sticky="w", pady=(10, 10), padx=10)
        reset_button_frame.grid_propagate(False)

        reset_equation_button = ctk.CTkButton(reset_button_frame, width=65, height=30, command=self.reset_equation,
                                              text="Reset", font=("Arial", 10, "bold"), fg_color=BLUE_COLOUR,
                                              hover_color=DARK_BLUE_COLOUR)
        reset_equation_button.grid(row=0, column=0, sticky="n", pady=9, padx=22)

    def show_reagent_moles(self):
        self.reagent_results_outer_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=540, height=300)
        self.reagent_results_outer_frame.grid(row=3, column=0, sticky="w", pady=(10, 10), padx=(20, 10))
        self.reagent_results_outer_frame.grid_propagate(False)

        reagent_results_title = ctk.CTkLabel(self.reagent_results_outer_frame, fg_color="white", text="Reagent Calculations",
                                             text_color="black", font=("Arial", 16, "bold"), anchor="w")
        reagent_results_title.grid(row=0, column=0, sticky="w", pady=(15, 15), padx=(15, 5))

        reagent_results_inner_frame = ctk.CTkFrame(self.reagent_results_outer_frame, fg_color=GRAY_COLOUR, corner_radius=15, width=500, height=220)
        reagent_results_inner_frame.grid(row=1, column=0, sticky="w", pady=(2, 15), padx=20)
        reagent_results_inner_frame.grid_propagate(False)

        titles = ["Reagent", "Molar Mass", "Mass (g)", "Moles", "Ratio", "Is the limiting reagent?"]
        limiting_reagent = self.determine_limiting_reagent()
        for j, title in enumerate(titles):
            if j == 0:
                padx_rule = (20, 5)
            elif j == len(titles):
                padx_rule = (5, 20)
            else:
                padx_rule = (5, 5)

            reagent_title = ctk.CTkLabel(reagent_results_inner_frame, text=title, text_color="black", fg_color=GRAY_COLOUR,
                                                 font=("Arial", 14, "bold"), anchor="w")
            reagent_title.grid(row=0, column=j, sticky="w", pady=(15, 5), padx=padx_rule)

        for i, reagent in enumerate(self.reagents, start=1):
            if i == 1:
                pady_rule = (10, 5)
            elif i == len(self.reagents):
                pady_rule = (5, 15)
            else:
                pady_rule = (5, 5)

            reagent_results_formula = ctk.CTkLabel(reagent_results_inner_frame, fg_color=GRAY_COLOUR, text=reagent["formula"],
                                                   text_color="black", font=("Arial", 13), anchor="w")
            reagent_results_formula.grid(row=i, column=0, sticky="w", pady=pady_rule, padx=(20, 5))

            reagent_results_molar_mass = ctk.CTkLabel(reagent_results_inner_frame, fg_color=GRAY_COLOUR, text=f"{reagent["molar mass"]:.2f}",
                                                      text_color="black", font=("Arial", 13), anchor="w")
            reagent_results_molar_mass.grid(row=i, column=1, sticky="w", pady=pady_rule, padx=5)

            reagent_results_mass = ctk.CTkLabel(reagent_results_inner_frame, fg_color=GRAY_COLOUR, text=reagent["mass"],
                                                text_color="black", font=("Arial", 13), anchor="w")
            reagent_results_mass.grid(row=i, column=2, sticky="w", pady=pady_rule, padx=5)

            reagent_results_moles = ctk.CTkLabel(reagent_results_inner_frame, fg_color=GRAY_COLOUR, text=f"{reagent['moles']:.3f}",
                                                 text_color="black", font=("Arial", 13), anchor="w")
            reagent_results_moles.grid(row=i, column=3, sticky="w", pady=pady_rule, padx=(5, 5))

            reagent_results_ratio = ctk.CTkLabel(reagent_results_inner_frame, fg_color=GRAY_COLOUR, text=f"{reagent['ratio']:.3f}",
                                                 text_color="black", font=("Arial", 13), anchor="w")
            reagent_results_ratio.grid(row=i, column=4, sticky="w", pady=pady_rule, padx=(5, 5))

            if reagent == limiting_reagent:
                reagent_results_moles = ctk.CTkLabel(reagent_results_inner_frame, fg_color=GRAY_COLOUR, text=f"Limiting Reagent",
                                                     text_color="black", font=("Arial", 13), anchor="w")
                reagent_results_moles.grid(row=i, column=5, sticky="w", pady=pady_rule, padx=(5, 20))
            else:
                reagent_results_moles = ctk.CTkLabel(reagent_results_inner_frame, fg_color=GRAY_COLOUR, text=f"Not the limiting reagent",
                                                     text_color="black", font=("Arial", 13), anchor="w")
                reagent_results_moles.grid(row=i, column=5, sticky="w", pady=pady_rule, padx=(5, 20))

    def show_product_moles(self):
        if not self.products or self.main_product.get() >= len(self.products):
            return

        self.product_results_outer_frame = ctk.CTkFrame(self.window, fg_color="white", corner_radius=15, width=300, height=300)
        self.product_results_outer_frame.grid(row=3, column=1, sticky="w", pady=(10, 10), padx=(10, 10))
        self.product_results_outer_frame.grid_propagate(False)

        product_results_title = ctk.CTkLabel(self.product_results_outer_frame, fg_color="white", text="Main Product",
                                             text_color="black", font=("Arial", 16, "bold"), anchor="w")
        product_results_title.grid(row=0, column=0, sticky="w", pady=(15, 15), padx=(15, 5))

        product_results_inner_frame = ctk.CTkFrame(self.product_results_outer_frame, fg_color=GRAY_COLOUR, corner_radius=15, width=260, height=220)
        product_results_inner_frame.grid(row=1, column=0, sticky="w", pady=(5, 15), padx=20)
        product_results_inner_frame.grid_propagate(False)

        selected_index = self.main_product.get()
        main_product = self.products[selected_index]

        main_product_formula = ctk.CTkLabel(product_results_inner_frame, fg_color=GRAY_COLOUR, text=f"{main_product["formula"]}",
                                               text_color="black", font=("Arial", 15, "bold"), anchor="w", justify="left")
        main_product_formula.grid(row=0, column=0, columnspan=2, pady=(20, 5), padx=20)

        main_product_molar_mass_label = ctk.CTkLabel(product_results_inner_frame, fg_color=GRAY_COLOUR, text="Molar Mass:",
                                                  text_color="black", font=("Arial", 13, "bold"), anchor="w", justify="left")
        main_product_molar_mass_label.grid(row=1, column=0, sticky="w", pady=2, padx=20)

        main_product_molar_mass = ctk.CTkLabel(product_results_inner_frame, fg_color=GRAY_COLOUR, text=f"{main_product["molar mass"]:.2f} g/mol",
                                               text_color="black", font=("Arial", 13), anchor="w", justify="left")
        main_product_molar_mass.grid(row=1, column=1, sticky="w", pady=2, padx=20)

        main_product_theoretical_mass_label = ctk.CTkLabel(product_results_inner_frame, fg_color=GRAY_COLOUR, text=f"Theoretical Mass:",
                                                     text_color="black", font=("Arial", 13, "bold"), anchor="w", justify="left")
        main_product_theoretical_mass_label.grid(row=2, column=0, sticky="w", pady=2, padx=20)

        main_product_theoretical_mass = ctk.CTkLabel(product_results_inner_frame, fg_color=GRAY_COLOUR, text=f"{main_product["theoretical mass"]:.3f} g",
                                                     text_color="black", font=("Arial", 13), anchor="w", justify="left")
        main_product_theoretical_mass.grid(row=2, column=1, sticky="w", pady=2, padx=20)

        main_product_actual_mass_label = ctk.CTkLabel(product_results_inner_frame, fg_color=GRAY_COLOUR, text=f"Actual Mass:",
                                                      text_color="black", font=("Arial", 13, "bold"), anchor="w", justify="left")
        main_product_actual_mass_label.grid(row=3, column=0, sticky="w", pady=2, padx=20)

        main_product_actual_mass = ctk.CTkLabel(product_results_inner_frame, fg_color=GRAY_COLOUR, text=f"{main_product["actual mass"]:.3f} g",
                                                text_color="black", font=("Arial", 13), anchor="w", justify="left")
        main_product_actual_mass.grid(row=3, column=1, sticky="w", pady=2, padx=20)

        main_product_results_moles_label = ctk.CTkLabel(product_results_inner_frame, fg_color=GRAY_COLOUR, text=f"Moles:",
                                                        text_color="black", font=("Arial", 13, "bold"), anchor="w", justify="left")
        main_product_results_moles_label.grid(row=4, column=0, sticky="w", pady=(2, 20), padx=20)

        main_product_results_moles = ctk.CTkLabel(product_results_inner_frame, fg_color=GRAY_COLOUR, text=f"{main_product['moles']:.3f} mol",
                                                  text_color="black", font=("Arial", 13), anchor="w",  justify="left")
        main_product_results_moles.grid(row=4, column=1, sticky="w", pady=(2, 20), padx=20)

    def show_percentage_yield(self):
        if not self.products or self.main_product.get() >= len(self.products):
            return

        self.percent_yield_results_outer_frame = ctk.CTkFrame(self.window, fg_color=BLUE_COLOUR, corner_radius=15)
        self.percent_yield_results_outer_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 10), padx=(20, 10))

        percent_yield_title = ctk.CTkLabel(self.percent_yield_results_outer_frame, fg_color=BLUE_COLOUR, text="Percent Yield and Analysis",
                                           text_color="white", font=("Arial", 14, "bold"), anchor="w")
        percent_yield_title.grid(row=0, column=0, sticky="w", pady=(10, 0), padx=(15, 15))

        percent_yield_results_inner_frame = ctk.CTkFrame(self.percent_yield_results_outer_frame, fg_color="white",
                                                              corner_radius=15, width=500, height=50)
        percent_yield_results_inner_frame.grid(row=1, column=0, sticky="ew", pady=(5, 15), padx=20)
        percent_yield_results_inner_frame.grid_propagate(False)

        selected_index = self.main_product.get()
        main_product = self.products[selected_index]
        percent_yield_value = main_product["percent yield"]

        if percent_yield_value <= 70:
            percent_yield_results_description = "Lower yield - consider optimizing conditions"
            result_colour = "#A50801"
        elif 70 < percent_yield_value <= 90:
            percent_yield_results_description = "Good yield for most organic reactions"
            result_colour = "#D4A502"
        elif 90 < percent_yield_value <= 100:
            percent_yield_results_description = "Excellent yield! Very efficient reaction"
            result_colour = "#136F05"
        elif percent_yield_value > 100:
            percent_yield_results_description = "Warning: Yield over 100% may indicate experimental error"
            result_colour = "#A50801"

        percent_yield_calculations = ctk.CTkLabel(percent_yield_results_inner_frame, fg_color="white",
                                                  text=f"{percent_yield_value:.2f}%", text_color=result_colour,
                                                  font=("Arial", 12), justify="left")
        percent_yield_calculations.grid(row=0, column=0, sticky="w", pady=10, padx=20)

        percent_yield_analysis = ctk.CTkLabel(percent_yield_results_inner_frame, fg_color="white",
                                              text=percent_yield_results_description, text_color=result_colour,
                                              font=("Arial", 12), justify="left")
        percent_yield_analysis.grid(row=0, column=1, sticky="w", pady=10, padx=20)

        percent_yield_title = ctk.CTkLabel(self.percent_yield_results_outer_frame, fg_color=BLUE_COLOUR,
                                           text="Formula", text_color="white", font=("Arial", 14, "bold"), anchor="w")
        percent_yield_title.grid(row=0, column=1, sticky="w", pady=(10, 0), padx=(15, 15))

        percent_yield_formula_inner_frame = ctk.CTkFrame(self.percent_yield_results_outer_frame, fg_color="white",
                                                              corner_radius=15, width=280, height=50)
        percent_yield_formula_inner_frame.grid(row=1, column=1, sticky="ew", pady=(5, 15), padx=20)
        percent_yield_formula_inner_frame.grid_propagate(False)

        percent_yield_calculations_description = ctk.CTkLabel(percent_yield_formula_inner_frame, fg_color="white",
                                                              text="% Yield = (Actual/Theoretical) × 100%",
                                                              text_color="black", font=("Arial", 12), justify="left")
        percent_yield_calculations_description.grid(row=0, column=0, sticky="w", pady=10, padx=20)

    def show_detailed_general_information(self):
        self.information_frame = ctk.CTkFrame(self.window, fg_color=BACKGROUND_COLOUR, corner_radius=15)
        self.information_frame.grid(row=0, column=2, sticky="ew", rowspan=5, pady=(10, 10), padx=0)

        concept_of_yield_outer_frame = ctk.CTkFrame(self.information_frame, fg_color="white", corner_radius=15, width=355, height=190)
        concept_of_yield_outer_frame.grid(row=0, sticky="w", pady=(10, 10), padx=15)
        concept_of_yield_outer_frame.grid_propagate(False)

        concept_of_yield_inner_frame = ctk.CTkFrame(concept_of_yield_outer_frame, fg_color=BLUE_COLOUR, corner_radius=15, width=325, height=170)
        concept_of_yield_inner_frame.grid(row=0, sticky="w", pady=(10, 10), padx=15)
        concept_of_yield_inner_frame.grid_propagate(False)

        basic_concepts_title = ctk.CTkLabel(concept_of_yield_inner_frame, fg_color=BLUE_COLOUR, text="Basic Concepts of Chemical Yield",
                                            text_color="white", font=("Arial", 16, "bold"), anchor="w")
        basic_concepts_title.grid(row=0, column=0, sticky="w", pady=(15, 0), padx=15)

        basic_concepts_description = ctk.CTkLabel(concept_of_yield_inner_frame, fg_color=BLUE_COLOUR,
                                                  text="• Actual Yield: This is the amount of product you actually collect.\n"
                                                       "• Theoretical Yield: This is the maximum amount of product that could be formed.\n"
                                                       "• Percent Yield: This tells you how efficient your reaction was.\n"
                                                       "• Limiting Reagent: The reactant in the reaction that will run out before the others.\n",
                                                  text_color="white", font=("Arial", 12), wraplength=305, anchor="w", justify="left")
        basic_concepts_description.grid(row=1, column=0, sticky="w", pady=(5, 10), padx=15)

        factors_affecting_yield_outer_frame = ctk.CTkFrame(self.information_frame, fg_color="white", corner_radius=15, width=355, height=160)
        factors_affecting_yield_outer_frame.grid(row=1, sticky="w", pady=(10, 10), padx=15)
        factors_affecting_yield_outer_frame.grid_propagate(False)

        factors_affecting_yield_inner_frame = ctk.CTkFrame(factors_affecting_yield_outer_frame, fg_color=GRAY_COLOUR, corner_radius=15, width=325, height=140)
        factors_affecting_yield_inner_frame.grid(row=0, sticky="w", pady=(10, 15), padx=15)
        factors_affecting_yield_inner_frame.grid_propagate(False)

        factors_yield_title = ctk.CTkLabel(factors_affecting_yield_inner_frame, fg_color=GRAY_COLOUR, text="Factors Affecting Reaction Yield",
                                            text_color="black", font=("Arial", 16, "bold"), anchor="w")
        factors_yield_title.grid(row=0, column=0, sticky="w", pady=(15, 0), padx=15)

        factors_yield_description = ctk.CTkLabel(factors_affecting_yield_inner_frame, fg_color=GRAY_COLOUR,
                                                  text="1. Side Reactions\n"
                                                       "2. Incomplete Reactions\n"
                                                       "3. Product Loss\n"
                                                       "4. Reaction Conditions\n"
                                                       "5. Equilibrium Limitations\n",
                                                  text_color="black", font=("Arial", 12), wraplength=300,
                                                  anchor="w", justify="left")
        factors_yield_description.grid(row=1, column=0, sticky="w", pady=(5, 10), padx=15)

        types_of_yield_outer_frame = ctk.CTkFrame(self.information_frame, fg_color="white", corner_radius=15, width=355, height=200)
        types_of_yield_outer_frame.grid(row=2, sticky="w", pady=(10, 10), padx=15)
        types_of_yield_outer_frame.grid_propagate(False)

        types_of_yield_inner_frame = ctk.CTkFrame(types_of_yield_outer_frame, fg_color=BLUE_COLOUR, corner_radius=15, width=325, height=180)
        types_of_yield_inner_frame.grid(row=0, sticky="w", pady=(10, 15), padx=15)
        types_of_yield_inner_frame.grid_propagate(False)

        factors_yield_title = ctk.CTkLabel(types_of_yield_inner_frame, fg_color=BLUE_COLOUR, text="Different Types of Yields",
                                           text_color="white", font=("Arial", 16, "bold"), anchor="w")
        factors_yield_title.grid(row=0, column=0, sticky="w", pady=(15, 0), padx=15)

        factors_yield_description = ctk.CTkLabel(types_of_yield_inner_frame, fg_color=BLUE_COLOUR,
                                                  text="• Chemical Yield: The general term for the amount of product obtained from a chemical reaction.\n"
                                                       "• Isolated Yield: The amount of purified product obtained after all separation and purification steps.\n"
                                                       "• Crude Yield: The amount of product obtained before any purification.\n"
                                                       "• Overall Yield: In multi-step reactions, this is the total yield from start to finish.\n",
                                                  text_color="white", font=("Arial", 12), wraplength=305,
                                                   anchor="w", justify="left")
        factors_yield_description.grid(row=1, column=0, sticky="w", pady=(5, 10), padx=15)

    def remove_reagent_product_frames(self):
        for widget_name in ["number_of_reagents_frame", "types_of_reagents_outer_frame",
                            "number_of_products_frame", "types_of_products_outer_frame", "buttons_frame", "errors_frame"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def remove_equation_results_frames(self):
        for widget_name in ["equation_outer_frame", "reagent_results_outer_frame",
                            "product_results_outer_frame", "percent_yield_results_outer_frame", "information_frame"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def reset_detailed_options(self):
        self.window.geometry("660x330")
        self.remove_reagent_product_frames()
        self.ask_calculation_mode()

    def reset_equation(self):
        self.window.state("normal")
        self.window.geometry("1170x600")
        self.remove_equation_results_frames()
        self.ask_reagent_count()
        self.ask_product_count()

    def remove_error_message(self):
        if self.error_label is not None:
            self.error_label.destroy()
            setattr(self, "error_label", None)

        if hasattr(self, "reagents_error_label") and self.reagents_error_label:
            self.reagents_error_label.destroy()
            self.reagents_error_label = None

        if hasattr(self, "products_error_label") and self.products_error_label:
            self.products_error_label.destroy()
            self.products_error_label = None

if __name__ == "__main__":
    root = ctk.CTk()
    app = ReactionYieldPredictor(root)
    root.mainloop()
