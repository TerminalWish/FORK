from fork_core import app, db, Menu, Ingredient, MenuIngredient


with app.app_context():
    # Define all menu items with name, description, and category
    menu_items = [
        # Drinks
        {"name": "Mystic Forest Manhattan", "description": "Rich rye whiskey blended with a deep forest essence, vermouth, and a dash of bitters, garnished with a mystical berry that blooms in the glass.", "category": "Drink"},
        {"name": "Wraith’s Whisper Whiskey Sour", "description": "Smooth whiskey with a wraithberry reduction, shaken with lemon juice and egg white, topped with a spectral mist that hovers above the glass.", "category": "Drink"},
        {"name": "Faerie Fizz", "description": "A bright, bubbly gin fizz with faerie-dust-infused gin, a hint of wild honey, and a slight shimmer that dances with each sip.", "category": "Drink"},
        {"name": "Blood Moon Sangria", "description": "Red wine and enchanted citrus, blended with midnight berries and a splash of basilisk bitters, served in a crystal goblet under a faint red glow.", "category": "Drink"},
        {"name": "Thunderstrike Mule", "description": "Vodka with a dash of thunder-charged ginger beer, served with a crackling ice cube that releases gentle, tingling sparks as you drink.", "category": "Drink"},
        {"name": "Mountainheart Barrel-Aged Manhattan", "description": "Rye whiskey aged in mountain oak barrels, mixed with vermouth and enchanted bitters, served with a twist of charred orange peel for a smoky, bold finish.", "category": "Drink"},
        {"name": "Stoneforge Stout", "description": "A dark, rich dwarven stout with roasted malt, smoked barley, and caramel undertones, a full-bodied brew that feels forged in the heart of a mountain.", "category": "Drink"},
        {"name": "Mountain King’s Mead", "description": "A classic dwarven mead made from mountain wildflowers and honey, aged to perfection, bringing a balanced sweetness and warmth to every sip.", "category": "Drink"},
        {"name": "Faerie Blossom Lemonade", "description": "A bright, pink lemonade made with enchanted blossoms, giving it a slight sparkle and a hint of natural sweetness, perfect for a refreshing drink with a touch of whimsy.", "category": "Drink"},
        {"name": "Sunlit Peach Nectar", "description": "A sweet and refreshing peach nectar with hints of vanilla and chamomile, served chilled and known to lift spirits with its summery flavor and soft golden hue.", "category": "Drink"},
        {"name": "Enchanted Cucumber Mint Elixir", "description": "A crisp cucumber and mint drink with a touch of elderflower, served over ice and garnished with a tiny enchanted flower that floats delicately on the surface.", "category": "Drink"},
        {"name": "Celestial Berry Spritzer", "description": "A sparkling berry spritzer with notes of blackberry, raspberry, and a hint of starfruit, topped with a touch of edible stardust for a magical shimmer.", "category": "Drink"},

        # Appetizers
        {"name": "Griffin Wing Drummies", "description": "Juicy, spiced wings from a Griffin, cooked to a perfect crisp and served with a basilisk-basil dipping sauce.", "category": "Appetizer"},
        {"name": "Pixie Poppers", "description": "Mini, herb-stuffed peppers with a light crunch, sprinkled with faerie dust for a hint of sweetness.", "category": "Appetizer"},
        {"name": "Phoenix Fire Fries", "description": "Crispy fries tossed in a fiery, spicy seasoning, served with a cooling enchanted blue cheese dip.", "category": "Appetizer"},
        {"name": "Golden Harvest Cauldron", "description": "A thick and creamy pumpkin and butternut squash soup with a hint of honey and warming spices. Served in mini cauldrons with a sprinkle of stardust.", "category": "Appetizer"},
        {"name": "Stormcloud Soup Shots", "description": "A smoky, dark potato and leek soup, swirled with charcoal cream, giving a stormy appearance and a bold, savory flavor.", "category": "Appetizer"},

        # Entrees
        {"name": "Dragon Tail Medallions", "description": "Small, tender pieces from the tail, ideal for rich sauces.", "category": "Entree"},
        {"name": "Basilisk Sirloin", "description": "Dense and flavorful, often said to carry a hint of petrifying power.", "category": "Entree"},
        {"name": "Kraken Calamari Steaks", "description": "Tender, thick slices from the Kraken’s arms, with a touch of the sea.", "category": "Entree"},
        {"name": "Minotaur Prime Rib", "description": "A massive, marbled cut, hearty and robust, perfect for slow roasting.", "category": "Entree"},
        {"name": "Leviathan Filet", "description": "A smooth, succulent filet with hints of deep-sea minerals, said to be quite rare.", "category": "Entree"},
        {"name": "Ethereal Venison", "description": "Derived from spirit deer, a delicate, airy meat with a whisper of sweetness.", "category": "Entree"},
        {"name": "Ancient Sea Dragon Bisque", "description": "A luxurious, creamy bisque made from rare dragon-scale shellfish, giving it a shimmering green hue. Rich in flavor and texture, this bisque is topped with a whisper of smoke from dragon-pepper oil.", "category": "Entree"},

        # Sides
        {"name": "Dwarven Ale-Braised Root Vegetables", "description": "A hearty mix of root vegetables, slow-cooked in rich dwarven ale, adding a touch of malty sweetness and warmth.", "category": "Side"},
        {"name": "Celestial Garlic Bread", "description": "Thick-cut garlic bread, charred and topped with a buttery garlic spread and a sprinkle of stardust, making it practically melt in your mouth.", "category": "Side"},
        {"name": "Dragon’s Breath Scalloped Potatoes", "description": "Layered potatoes with a rich, fiery cheese sauce that brings a warm, lingering heat to every bite.", "category": "Side"},
        {"name": "Sorcerer’s Saffron Rice", "description": "Golden-hued rice infused with rare saffron and enchanted spices, offering a warm and aromatic depth to complement any main.", "category": "Side"},
        {"name": "Moonlit Mashed Potatoes", "description": "Creamy mashed potatoes with a subtle sweetness and a faint, ethereal glow inspired by the light of the moon.", "category": "Side"},
        {"name": "Thunderstorm Brussels Sprouts", "description": "Charred Brussels sprouts tossed in a zesty, lightning-infused glaze, giving a bold flavor and satisfying crunch.", "category": "Side"},

        # Desserts
        {"name": "Dragonfire Crème Brûlée", "description": "A classic crème brûlée infused with a hint of dragon-pepper, giving it a subtle heat beneath the caramelized sugar top. The crust crackles with a faint, warm glow when served.", "category": "Dessert"},
        {"name": "Wizard’s Molten Chocolate Tower", "description": "A rich, dark chocolate cake shaped like a miniature wizard’s tower, with a molten center that flows like enchanted lava. Each bite is infused with a hint of midnight mint and a dusting of powdered crystal, giving it an air of mystical decadence and the strength of ancient spells.", "category": "Dessert"},
        {"name": "Elven Honey Cake", "description": "A delicate, layered cake made with honey from enchanted elven hives, topped with edible flowers and a whipped cream infused with a touch of faerie dust.", "category": "Dessert"},
        {"name": "Enchanted Sorbet - Frosted Berry", "description": "A blend of enchanted wild berries with a subtle sparkle, perfect for a cool, fruity treat.", "category": "Dessert"},
        {"name": "Enchanted Sorbet - Celestial Citrus", "description": "A bright, zesty sorbet made with enchanted lemon and starfruit, offering a balance of tart and sweet.", "category": "Dessert"},
        {"name": "Enchanted Sorbet - Gilded Peach", "description": "A velvety peach sorbet with hints of vanilla and a soft golden hue, capturing the sweetness of a summer day.", "category": "Dessert"},
    ]

    # # Populate the Menu table with each item
    # for item in menu_items:
    #     menu_entry = Menu(name=item["name"], description=item["description"], category=item["category"])
    #     db.session.add(menu_entry)

    # # Commit all items to the database
    # db.session.commit()

    ingredient_names = [
        "Enchanted Blossom Syrup", "Fresh Lemon Juice", "Water", "Sparkling Water", 
        "Honey", "Edible Glitter Dust", "Peach Puree", "Chamomile-Infused Water", 
        "Vanilla Extract", "Cucumber Juice", "Fresh Mint Leaves", "Elderflower Syrup", 
        "Ice Cubes", "Tiny Edible Flower", "Blackberry Juice", "Raspberry Juice", 
        "Starfruit Juice", "Griffin Wing Meat", "Phoenix Fire Pepper Flakes", 
        "Dark Forest Honey", "Fresh Basil Leaves", "Olive Oil", "Smoked Salt", 
        "Greek Yogurt", "Lemon Juice", "Essence of Basilisk Root", "Ground Paprika", 
        "Mini Sweet Peppers", "Fresh Thyme", "Crumbled Goat Cheese", "Starflower Petals", 
        "Enchanted Honey", "Flaked Sea Salt", "Russet Potatoes", "Sun-blessed Sunflower Oil", 
        "Ember Ash", "Cayenne Pepper", "Black Volcanic Salt", "Crushed Inferno Peppercorns", 
        "Crumbled Blue Cheese", "Dried Moon Herb", "Pumpkin Purée", "Butternut Squash Purée", 
        "Heavy Cream", "Ground Cinnamon", "Starfall Sugar", "Nutmeg", "Silver Thyme", 
        "Stardust", "Leek", "Vegetable Broth", "Activated Charcoal Powder", 
        "Mistleaf Essence", "Storm Salt", "Dragon Tail Meat", "Dragonberry Reduction", 
        "Butter", "Smoked Paprika", "Crushed Ruby Salt", "Ground Thyme", "Fresh Parsley", 
        "Ember Dust", "Basilisk Sirloin Steak", "Dark Forest Soy", "Black Peppercorn", 
        "Petrified Herb Blend", "Sea Salt", "Ember Pepper Flakes", "Fresh Rosemary", 
        "Kraken Arm Slices", "Brine Salt", "Ground Basil Leaves", "Whisper Kelp Flakes", 
        "Aioli", "Mistflower Essence", "Minotaur Prime Rib", "Wild Sage", 
        "Phoenix Ember Dust", "Beef Broth", "Roasted Garlic Clove", "Enchanted Red Wine", 
        "Leviathan Filet", "Lemon Zest", "Crushed Seaweed Flakes", 
        "Spirit Deer Venison", "Blueberry Reduction", "Cloud Pepper", 
        "Dragon-scale Shellfish", "Shimmering Leek", "Garlic", "Crushed Dragon-pepper", 
        "Crushed Saffron Threads", "Fennel Fronds", "Root Vegetable Mix", "Dwarven Ale", 
        "Onion", "Mountain Salt", "Thick-cut Bread Slices", "Chopped Parsley", 
        "Fiery Cheese Blend", "Chives", "Basmati Rice", "Bay Leaf", "Yukon Gold Potatoes", 
        "Moonbeam Salt", "White Pepper", "Brussels Sprouts", "Lightning Zest Glaze", 
        "Dark Chocolate", "Sugar", "Flour", "Midnight Mint Essence", "Powdered Crystal Dust", 
        "Edible Flowers", "Mixed Enchanted Wild Berries", 
        "Lemon Juice", "Starfruit Puree", "Gold Dust", "Faerie Dust", "Frying Oil", "Dill", "Cracked Black Pepper",
        "Vegetable Stock", "Sharp Cheddar Cheese", "Dragon-Pepper Cheese", "Crushed Red Pepper Flakes", "Ember Salt",
        "Enchanted Spice Blend", "Eggs", "Granulated Sugar", "Vanilla Bean", "Ember Crystals", "Baking Powder",
        "Whipped Cream", "Blackberries", "Enchanted Snowberries", "Enchanted Lemon Juice", "Fresh Peach Puree"
    ]

    # Insert each unique ingredient into the database
    for ingredient_name in ingredient_names:
        # Check if the ingredient already exists in the database
        existing_ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if not existing_ingredient:
            # If it doesn't exist, add it
            ingredient = Ingredient(name=ingredient_name)
            db.session.add(ingredient)

    # Commit all changes
    db.session.commit()

    menu_ingredient_data = {
        "Faerie Blossom Lemonade": [
            ("Enchanted Blossom Syrup", 2, "tbsp"),
            ("Fresh Lemon Juice", 0.25, "cup"),
            ("Water", 1, "cup"),
            ("Sparkling Water", 0.5, "cup"),
            ("Honey", 1, "tsp"),
            ("Edible Glitter Dust", 0.0052, "oz"),
        ],
        "Sunlit Peach Nectar": [
            ("Peach Puree", 0.33, "cup"),
            ("Chamomile-Infused Water", 0.25, "cup"),
            ("Vanilla Extract", 0.125, "tsp"),
            ("Honey", 1, "tbsp"),
            ("Water", 0.33, "cup"),
        ],
        "Enchanted Cucumber Mint Elixir": [
            ("Cucumber Juice", 0.33, "cup"),
            ("Fresh Mint Leaves", 0.06, "oz"),
            ("Elderflower Syrup", 1, "tbsp"),
            ("Ice Cubes", 2, "oz"),
            ("Water", 0.5, "cup"),
            ("Tiny Edible Flower", 0.05, "oz"),
        ],
        "Celestial Berry Spritzer": [
            ("Blackberry Juice", 2, "tbsp"),
            ("Raspberry Juice", 2, "tbsp"),
            ("Starfruit Juice", 1, "tbsp"),
            ("Sparkling Water", 0.75, "cup"),
            ("Stardust", 0.01, "oz"),
        ],
        "Griffin Wing Drummies": [
            # Drummies
            ("Griffin Wing Meat", 12, "oz"),
            # Marinade
            ("Phoenix Fire Pepper Flakes", 0.25, "tsp"),
            ("Dark Forest Honey", 1, "tbsp"),
            ("Fresh Basil Leaves", 0.04, "oz"),
            ("Olive Oil", 1, "tbsp"),
            ("Smoked Salt", 0.03, "oz"),
            # Dipping Sauce
            ("Greek Yogurt", 0.5, "cup"),
            ("Lemon Juice", 1, "tbsp"),
            ("Essence of Basilisk Root", 0.125, "tsp"),
            ("Ground Paprika", 0.25, "tsp"),
        ],
        "Pixie Poppers": [
            # Peppers
            ("Mini Sweet Peppers", 3, "oz"),
            # Herb Stuffing
            ("Fresh Thyme", 0.5, "tsp"),
            ("Crumbled Goat Cheese", 0.25, "cup"),
            ("Starflower Petals", 0.25, "tsp"),
            ("Enchanted Honey", 1, "tsp"),
            ("Olive Oil", 1, "tsp"),
            # Topping
            ("Faerie Dust", 0.25, "tsp"),
            ("Flaked Sea Salt", 0.03, "oz"),
        ],
        "Phoenix Fire Fries": [
            # Fries
            ("Russet Potatoes", 20, "oz"),
            ("Frying Oil", 2, "cups"),
            # Fiery Seasoning
            ("Ember Ash", 0.125, "tsp"),
            ("Cayenne Pepper", 0.25, "tsp"),
            ("Black Volcanic Salt", 0.03, "oz"),
            ("Crushed Inferno Peppercorns", 0.25, "tsp"),
            # Cooling Blue Cheese Dip
            ("Crumbled Blue Cheese", 0.33, "cup"),
            ("Greek Yogurt", 0.25, "cup"),
            ("Dried Moon Herb", 0.125, "tsp"),
        ],
        "Golden Harvest Cauldron": [
            # Soup Base
            ("Pumpkin Purée", 1, "cup"),
            ("Butternut Squash Purée", 1, "cup"),
            ("Honey", 1, "tbsp"),
            ("Heavy Cream", 0.25, "cup"),
            # Warming Spices
            ("Ground Cinnamon", 0.25, "tsp"),
            ("Starfall Sugar", 1, "tsp"),
            ("Nutmeg", 0.125, "tsp"),
            ("Silver Thyme", 0.01, "oz"),
            ("Stardust", 0.125, "tsp"),
        ],
        "Stormcloud Soup Shots": [
            # Soup Base
            ("Russet Potatoes", 1, "cup"),
            ("Leek", 0.5, "cup"),
            ("Vegetable Broth", 1, "cup"),
            # Charcoal Cream Swirl
            ("Heavy Cream", 0.25, "cup"),
            ("Activated Charcoal Powder", 0.03, "oz"),
            ("Mistleaf Essence", 1, "drop"),
            ("Storm Salt", 0.125, "tsp"),
            ("Black Peppercorn", 0.03, "oz"),
        ],
        "Dragon Tail Medallions": [
            # Medallions
            ("Dragon Tail Meat", 8, "oz"),
            # Sauce
            ("Dragonberry Reduction", 2, "tbsps"),
            ("Butter", 1, "tbsp"),
            ("Smoked Paprika", 0.25, "tsp"),
            ("Crushed Ruby Salt", 0.125, "tsp"),
            ("Ground Thyme", 0.25, "tsp"),
            # Garnish
            ("Fresh Parsley", 0.5, "tsp"),
            ("Ember Dust", 0.03, "oz"),
        ],
        "Basilisk Sirloin": [
            # Sirloin
            ("Basilisk Sirloin Steak", 10, "oz"),
            # Marinade
            ("Dark Forest Soy", 1, "tbsp"),
            ("Black Peppercorn", 0.25, "tsp"),
            ("Petrified Herb Blend", 0.25, "tsp"),
            ("Olive Oil", 1, "tbsp"),
            # Rub
            ("Sea Salt", 0.03, "oz"),
            ("Ember Pepper Flakes", 0.03, "oz"),
            # Garnish
            ("Fresh Rosemary", 0.04, "oz"),
        ],
        "Kraken Calamari Steaks": [
            # Calamari
            ("Kraken Arm Slices", 6, "oz"),
            # Marinade
            ("Lemon Juice", 1, "tbsp"),
            ("Garlic", 0.5, "tsp"),
            ("Sea Salt", 0.125, "tsp"),
            # Seasoning
            ("Smoked Paprika", 0.25, "tsp"),
            ("Ground Basil Leaves", 0.25, "tsp"),
            ("Whisper Kelp Flakes", 0.125, "tsp"),
            # Dipping Sauce
            ("Aioli", 2, "tbsps"),
            ("Mistflower Essence", 0.05, "ml"),
        ],
        "Minotaur Prime Rib": [
            # Prime Rib
            ("Minotaur Prime Rib", 12, "oz"),
            # Seasoning Rub
            ("Cracked Black Pepper", 0.5, "tsp"),
            ("Sea Salt", 0.03, "oz"),
            ("Smoked Paprika", 0.25, "tsp"),
            ("Wild Sage", 0.125, "tsp"),
            ("Phoenix Ember Dust", 0.03, "oz"),
            # Au Jus
            ("Beef Broth", 0.5, "cup"),
            ("Fresh Thyme", 0.01, "oz"),
            ("Roasted Garlic Clove", 0.18, "oz"),
            ("Enchanted Red Wine", 1, "tbsp"),
        ],
        "Leviathan Filet": [
            # Filet
            ("Leviathan Filet", 8, "oz"),
            # Marinade
            ("Lemon Zest", 0.25, "tsp"),
            ("Sea Salt", 0.125, "tsp"),
            ("Olive Oil", 1, "tbsp"),
            # Seasoning
            ("Crushed Seaweed Flakes", 0.25, "tsp"),
            ("Smoked Salt", 0.03, "oz"),
            # Butter Glaze
            ("Butter", 1, "tbsp"),
            ("Dill", 0.25, "tsp"),
            ("Stardust", 0.125, "tsp"),
        ],
        "Ethereal Venison": [
            # Venison
            ("Spirit Deer Venison", 8, "oz"),
            # Marinade
            ("Honey", 1, "tbsp"),
            ("Fresh Rosemary", 0.05, "oz"),
            ("Cracked Black Pepper", 0.25, "tsp"),
            ("Fresh Thyme", 0.03, "oz"),
            # Sauce
            ("Blueberries", 1/4, "cup"),
            ("Butter", 1, "tsp"),
            ("Cloud Pepper", 0.03, "oz"),
        ],
        "Ancient Sea Dragon Bisque": [
            # Bisque Base
            ("Dragon-Scale Shellfish", 0.25, "cup"),
            ("Heavy Cream", 1, "cup"),
            ("Vegetable Stock", 0.5, "cup"),
            ("Shimmering Leek", 0.25, "cup"),
            ("Garlic", 0.11, "oz"),
            # Seasoning
            ("Crushed Dragon-Pepper", 0.03, "oz"),
            ("Sea Salt", 0.03, "oz"),
            ("Crushed Saffron Threads", 0.03, "oz"),
            # Garnish
            ("Smoked Paprika", 0.03, "oz"),
            ("Fennel Fronds", 0.05, "oz"),
        ],
        "Dwarven Ale-Braised Root Vegetables": [
            # Vegetables
            ("Root Vegetable Mix", 1, "cup"),
            ("Dwarven Ale", 0.5, "cup"),
            ("Vegetable Broth", 0.25, "cup"),
            ("Onion", 0.5, "cup"),
            ("Garlic", 0.2, "oz, minced"),
            ("Fresh Thyme", 0.25, "tsp"),
            ("Mountain Salt", 0.03, "oz"),
            ("Butter", 1, "tbsp"),
        ],
        "Celestial Garlic Bread": [
            # Garlic Bread
            ("Thick-Cut Bread Slices", 8, "oz"),
            ("Garlic", 0.2, "oz"),
            ("Butter", 2, "tbsps"),
            ("Stardust", 0.03, "oz"),
            ("Chopped Parsley", 1, "tsp"),
            ("Sea Salt", 0.03, "oz"),
        ],
        "Dragon’s Breath Scalloped Potatoes": [
            # Scalloped Potatoes
            ("Yukon Gold Potatoes", 24, "oz"),
            ("Sharp Cheddar Cheese", 3, "oz"),
            ("Dragon-Pepper Cheese", 1, "oz"),
            ("Crushed Red Pepper Flakes", 0.008, "oz"),
            ("Smoked Paprika", 0.05, "oz"),
            ("Heavy Cream", 0.5, "cup"),
            ("Butter", 1, "tbsp"),
            ("Ember Salt", 0.03, "oz"),
            ("Fresh Chives", 0.5, "tsp"),
        ],
        "Sorcerer’s Saffron Rice": [
            # Saffron Rice
            ("Basmati Rice", 1, "cup"),
            ("Crushed Saffron Threads", 0.03, "oz"),
            ("Enchanted Spice Blend", 0.25, "tsp"),
            ("Vegetable Broth", 1.5, "cups"),
            ("Bay Leaf", 0.02, "oz"),
            ("Sea Salt", 0.03, "oz"),
            ("Olive Oil", 1, "tbsp"),
        ],
        "Moonlit Mashed Potatoes": [
            ("Yukon Gold Potatoes", 24, "oz"),
            ("Heavy Cream", 0.25, "cup"),
            ("Butter", 2, "tbsps"),
            ("Moonbeam Salt", 0.03, "oz"),
            ("White Pepper", 0.125, "tsp"),
            ("Chives", 0.5, "tsp"),
        ],
        "Thunderstorm Brussels Sprouts": [
            ("Brussels Sprouts", 1, "cup"),
            ("Olive Oil", 1, "tbsp"),
            ("Lightning Zest Glaze", 0.5, "tsp"),
            ("Garlic", 0.11, "oz"),
            ("Sea Salt", 0.03, "oz"),
            ("Smoked Paprika", 0.125, "tsp"),
            ("Cracked Black Pepper", 0.03, "oz"),
        ],
        "Dragonfire Crème Brûlée": [
            ("Heavy Cream", 1, "cup"),
            ("Eggs", 4, "large"),
            ("Granulated Sugar", 0.25, "cup"),
            ("Dragon-Pepper Extract", 0.05, "ml"),
            ("Vanilla Bean", 0.1, "oz"),
            ("Ember Crystals", 0.03, "oz"),
        ],
        "Wizard’s Molten Chocolate Tower": [
            ("Dark Chocolate", 6, "oz"),
            ("Butter", 0.25, "cup"),
            ("Sugar", 0.33, "cup"),
            ("Eggs", 2, "large"),
            ("Flour", 0.25, "cup"),
            ("Midnight Mint Essence", 0.125, "tsp"),
            ("Powdered Crystal Dust", 0.03, "oz"),
        ],
        "Elven Honey Cake": [
            ("Flour", 1, "cup"),
            ("Honey", 0.33, "cup"),
            ("Butter", 0.25, "cup"),
            ("Eggs", 2, "large"),
            ("Baking Powder", 0.5, "tsp"),
            ("Vanilla Extract", 0.5, "tsp"),
            ("Whipped Cream", 1, "cup"),
            ("Faerie Dust", 0.03, "oz"),
            ("Edible Flowers", 0.2, "oz"),
        ],
        "Enchanted Sorbet - Frosted Berry": [
            ("Blackberries", 0.33, "cup"),
            ("Blueberries", 0.33, "cup"),
            ("Enchanted Snowberries", 0.33, "cup"),
            ("Sugar", 0.25, "cup"),
            ("Water", 0.25, "cup"),
            ("Lemon Juice", 1, "tbsp"),
            ("Stardust", 0.03, "oz"),
        ],
        "Enchanted Sorbet - Celestial Citrus": [
            ("Enchanted Lemon Juice", 0.5, "cup"),
            ("Starfruit Puree", 0.25, "cup"),
            ("Sugar", 0.25, "cup"),
            ("Water", 0.25, "cup"),
            ("Stardust", 0.03, "oz"),
        ],
        "Enchanted Sorbet - Gilded Peach": [
            ("Fresh Peach Puree", 0.5, "cup"),
            ("Vanilla Bean", 0.25, "tsp, seeds scraped"),
            ("Sugar", 0.25, "cup"),
            ("Water", 0.25, "cup"),
            ("Gold Dust", 0.03, "oz"),
        ],
    }

    for menu_name, ingredients in menu_ingredient_data.items():
        # Find the menu item by name
        menu = Menu.query.filter_by(name=menu_name).first()
        if not menu:
            print(f"Menu item '{menu_name}' not found.")
            continue

        for ingredient_name, quantity, measurement in ingredients:
            # Find the ingredient by name
            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if not ingredient:
                print(f"Ingredient '{ingredient_name}' not found.")
                continue

            # Add to MenuIngredient
            menu_ingredient = MenuIngredient(
                menu_id=menu.id,
                ingredient_id=ingredient.id,
                quantity=quantity,
                measurement=measurement
            )
            db.session.add(menu_ingredient)

    # Commit all changes
    db.session.commit()

    # Close the session
    db.session.close()

