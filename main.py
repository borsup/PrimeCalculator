from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.core.window import Window
import random


class Tab(MDFloatLayout, MDTabsBase):
    pass


class MetalCalculatorApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = 'fr'
        self.translations = {
            'en': {
                'title': 'Metal Premium Calculator',
                'gold': 'Gold',
                'silver': 'Silver',
                'other': 'Other Metal',
                'about': 'About',
                'spot_price': 'Spot Price (€/gr)',
                'gross_weight': 'Gross Weight (gr)',
                'fineness': 'Fineness',
                'fine_weight': 'Fine Weight (gr)',
                'selling_price': 'Selling Price (€)',
                'premium': 'Premium',
                'refresh': 'Refresh',
                'calculate': 'Calculate',
                'error_required': 'Required field',
                'error_positive': 'Must be positive',
                'error_fineness': 'Must be between 0 and 1',
                'about_title': 'About This Calculator',
                'about_premium': 'What is the Premium?',
                'about_premium_text': 'The premium on gold (or any other physical precious metal such as silver) is the difference between the selling or buying price of a physical gold product and its intrinsic value in pure metal.',
                'about_use': 'How to Use',
                'about_use_text': 'Select the metal type, enter the gross weight, fineness (0-1), and selling price. The premium will be calculated automatically.',
                'developer': 'Developer: borsup',
            },
            'fr': {
                'title': 'Calculateur de Prime',
                'gold': 'Or',
                'silver': 'Argent',
                'other': 'Autre Métal',
                'about': 'A Propos',
                'spot_price': 'Cours (€/gr)',
                'gross_weight': 'Poids brut (gr)',
                'fineness': 'Titre',
                'fine_weight': 'Poids fin (gr)',
                'selling_price': 'Prix de vente (€)',
                'premium': 'Prime',
                'refresh': 'Actualiser',
                'calculate': 'Calculer',
                'error_required': 'Champ requis',
                'error_positive': 'Doit être positif',
                'error_fineness': 'Doit être entre 0 et 1',
                'about_title': 'À Propos',
                'about_premium': 'Qu\'est-ce qu\'une prime?',
                'about_premium_text': 'La prime sur l\'or (ou tout autre métal précieux physique) est la différence entre le prix de vente et sa valeur intrinsèque en métal pur.',
                'about_use': 'Comment utiliser',
                'about_use_text': 'Sélectionnez le type de métal, entrez le poids brut, le titre (0-1) et le prix de vente. La prime sera calculée automatiquement.',
                'developer': 'Développeur: borsup',
            }
        }

        # Store calculator inputs
        self.calculators = {
            'gold': {'spot': 111.2, 'gross': '', 'fineness': '', 'fine': '', 'selling': '', 'premium': None},
            'silver': {'spot': 1.58, 'gross': '', 'fineness': '', 'fine': '', 'selling': '', 'premium': None},
            'other': {'spot': '', 'gross': '', 'fineness': '', 'fine': '', 'selling': '', 'premium': None}
        }

    def t(self, key):
        return self.translations[self.language].get(key, key)

    def toggle_language(self, *args):
        self.language = 'en' if self.language == 'fr' else 'fr'
        self.rebuild_ui()

    def rebuild_ui(self):
        self.root.clear_widgets()
        self.root.add_widget(self.build_main_screen())

    def build(self):
        self.theme_cls.primary_palette = 'Amber'
        self.theme_cls.theme_style = 'Light'
        Window.size = (360, 640)

        return self.build_main_screen()

    def build_main_screen(self):
        screen = MDScreen()
        main_layout = MDBoxLayout(orientation='vertical')

        # Toolbar
        toolbar = MDTopAppBar(
            title=self.t('title'),
            md_bg_color=[0.95, 0.7, 0.2, 1],
            right_action_items=[["translate", lambda x: self.toggle_language()]]
        )
        main_layout.add_widget(toolbar)

        # Tabs
        tabs = MDTabs(
            on_tab_switch=self.on_tab_switch,
            background_color=[1, 1, 1, 1]
        )

        # Gold Tab
        gold_tab = Tab(title=self.t('gold'))
        gold_tab.add_widget(self.build_calculator('gold'))
        tabs.add_widget(gold_tab)

        # Silver Tab
        silver_tab = Tab(title=self.t('silver'))
        silver_tab.add_widget(self.build_calculator('silver'))
        tabs.add_widget(silver_tab)

        # Other Metal Tab
        other_tab = Tab(title=self.t('other'))
        other_tab.add_widget(self.build_calculator('other'))
        tabs.add_widget(other_tab)

        # About Tab
        about_tab = Tab(title=self.t('about'))
        about_tab.add_widget(self.build_about())
        tabs.add_widget(about_tab)

        main_layout.add_widget(tabs)
        screen.add_widget(main_layout)

        return screen

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pass

    def build_calculator(self, metal_type):
        scroll = MDScrollView()
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))

        data = self.calculators[metal_type]
        is_auto = metal_type in ['gold', 'silver']

        # Spot Price
        spot_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        spot_field = MDTextField(
            hint_text=self.t('spot_price'),
            text=str(data['spot']) if data['spot'] else '',
            disabled=is_auto,
            size_hint_x=0.8,
            mode='rectangle'
        )
        spot_field.metal_type = metal_type
        spot_field.field_name = 'spot'
        spot_field.bind(text=self.on_input_change)
        spot_layout.add_widget(spot_field)

        if is_auto:
            refresh_btn = MDIconButton(
                icon='refresh',
                on_release=lambda x: self.refresh_spot_price(metal_type, spot_field)
            )
            spot_layout.add_widget(refresh_btn)

        layout.add_widget(spot_layout)

        # Gross Weight
        gross_field = MDTextField(
            hint_text=self.t('gross_weight'),
            text=data['gross'],
            size_hint_y=None,
            height=dp(60),
            mode='rectangle'
        )
        gross_field.metal_type = metal_type
        gross_field.field_name = 'gross'
        gross_field.bind(text=self.on_input_change)
        layout.add_widget(gross_field)

        # Fineness
        fineness_field = MDTextField(
            hint_text=self.t('fineness'),
            text=data['fineness'],
            size_hint_y=None,
            height=dp(60),
            mode='rectangle'
        )
        fineness_field.metal_type = metal_type
        fineness_field.field_name = 'fineness'
        fineness_field.bind(text=self.on_input_change)
        layout.add_widget(fineness_field)

        # Fine Weight (Read-only)
        fine_field = MDTextField(
            hint_text=self.t('fine_weight'),
            text=data['fine'],
            disabled=True,
            size_hint_y=None,
            height=dp(60),
            mode='rectangle'
        )
        fine_field.metal_type = metal_type
        fine_field.field_name = 'fine'
        setattr(self, f'{metal_type}_fine_field', fine_field)
        layout.add_widget(fine_field)

        # Selling Price
        selling_field = MDTextField(
            hint_text=self.t('selling_price'),
            text=data['selling'],
            size_hint_y=None,
            height=dp(60),
            mode='rectangle'
        )
        selling_field.metal_type = metal_type
        selling_field.field_name = 'selling'
        selling_field.bind(text=self.on_input_change)
        layout.add_widget(selling_field)

        # Premium Display Card
        premium_card = MDCard(
            size_hint_y=None,
            height=dp(100),
            padding=dp(15),
            md_bg_color=[0.95, 0.95, 0.95, 1],
            radius=[15]
        )
        premium_layout = MDBoxLayout(orientation='vertical', spacing=dp(5))

        premium_label = MDLabel(
            text=self.t('premium'),
            size_hint_y=None,
            height=dp(30),
            font_style='H6'
        )
        premium_layout.add_widget(premium_label)

        premium_value = MDLabel(
            text='-- %',
            size_hint_y=None,
            height=dp(50),
            font_style='H3',
            bold=True
        )
        setattr(self, f'{metal_type}_premium_label', premium_value)
        premium_layout.add_widget(premium_value)

        premium_card.add_widget(premium_layout)
        layout.add_widget(premium_card)

        scroll.add_widget(layout)
        return scroll

    def build_about(self):
        scroll = MDScrollView()
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))

        # Title
        title = MDLabel(
            text=self.t('about_title'),
            font_style='H4',
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(title)

        # What is Premium Card
        card1 = MDCard(
            size_hint_y=None,
            height=dp(150),
            padding=dp(15),
            md_bg_color=[1, 0.95, 0.8, 1],
            radius=[10]
        )
        card1_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        card1_title = MDLabel(
            text=self.t('about_premium'),
            font_style='H6',
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        card1_text = MDLabel(
            text=self.t('about_premium_text'),
            size_hint_y=None,
            height=dp(100),
            text_size=(Window.width - dp(70), None)
        )
        card1_layout.add_widget(card1_title)
        card1_layout.add_widget(card1_text)
        card1.add_widget(card1_layout)
        layout.add_widget(card1)

        # How to Use Card
        card2 = MDCard(
            size_hint_y=None,
            height=dp(150),
            padding=dp(15),
            md_bg_color=[0.8, 0.95, 1, 1],
            radius=[10]
        )
        card2_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))
        card2_title = MDLabel(
            text=self.t('about_use'),
            font_style='H6',
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        card2_text = MDLabel(
            text=self.t('about_use_text'),
            size_hint_y=None,
            height=dp(100),
            text_size=(Window.width - dp(70), None)
        )
        card2_layout.add_widget(card2_title)
        card2_layout.add_widget(card2_text)
        card2.add_widget(card2_layout)
        layout.add_widget(card2)

        # Developer Card
        card3 = MDCard(
            size_hint_y=None,
            height=dp(80),
            padding=dp(15),
            md_bg_color=[0.9, 0.9, 0.9, 1],
            radius=[10]
        )
        dev_label = MDLabel(
            text=self.t('developer'),
            font_style='H6',
            bold=True
        )
        card3.add_widget(dev_label)
        layout.add_widget(card3)

        scroll.add_widget(layout)
        return scroll

    def refresh_spot_price(self, metal_type, field):
        base_prices = {'gold': 111.2, 'silver': 1.58}
        if metal_type in base_prices:
            variation = (random.random() - 0.5) * 2
            new_price = base_prices[metal_type] + variation
            field.text = f'{new_price:.2f}'
            self.calculators[metal_type]['spot'] = new_price

    def on_input_change(self, instance, value):
        metal_type = instance.metal_type
        field_name = instance.field_name

        # Update data
        self.calculators[metal_type][field_name] = value

        # Calculate fine weight
        data = self.calculators[metal_type]
        if data['gross'] and data['fineness']:
            try:
                gross = float(data['gross'])
                fineness = float(data['fineness'])
                fine = gross * fineness
                data['fine'] = f'{fine:.3f}'
                fine_field = getattr(self, f'{metal_type}_fine_field', None)
                if fine_field:
                    fine_field.text = data['fine']
            except ValueError:
                data['fine'] = ''

        # Calculate premium
        if data['spot'] and data['fine'] and data['selling']:
            try:
                spot = float(data['spot'])
                fine = float(data['fine'])
                selling = float(data['selling'])

                if spot > 0 and fine > 0:
                    intrinsic = fine * spot
                    premium = ((selling - intrinsic) / intrinsic) * 100
                    data['premium'] = premium

                    premium_label = getattr(self, f'{metal_type}_premium_label', None)
                    if premium_label:
                        premium_label.text = f'{premium:.2f} %'

                        # Set color based on premium
                        if premium <= 10:
                            premium_label.color = [0, 0.7, 0, 1]  # Green
                        elif premium <= 15:
                            premium_label.color = [1, 0.6, 0, 1]  # Orange
                        else:
                            premium_label.color = [1, 0, 0, 1]  # Red
            except (ValueError, ZeroDivisionError):
                pass


if __name__ == '__main__':
    MetalCalculatorApp().run()

