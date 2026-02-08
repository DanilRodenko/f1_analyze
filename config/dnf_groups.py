
STATUS_FINISHED = {
    'Finished': [1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 45, 50,
                 53, 55, 58, 88, 111, 112, 113, 114, 115, 116, 117,
                 118, 119, 120, 122, 123, 124, 125, 127, 128, 133, 134],
    'NotFinishedNotDNF': [28, 68, 73, 81, 82, 90, 93, 97, 100, 107, 136, 139]
}

STATUS_FINISHED['DNF'] = [
    i for i in range(1, 142)
    if i not in STATUS_FINISHED['Finished'] and i not in STATUS_FINISHED['NotFinishedNotDNF']
]


DNF_GROUPS  = {
    "Mechanical Failure": [
        "Alternator", "Axle", "Battery", "Brake duct", "Brakes", "CV joint", "Chassis",
        "Clutch", "Cooling system", "Crankshaft", "Differential", "Distributor",
        "Driveshaft", "Drivetrain", "ERS", "Electrical", "Electronics", "Engine",
        "Engine fire", "Engine misfire", "Exhaust", "Fuel", "Fuel leak", "Fuel pipe",
        "Fuel pressure", "Fuel pump", "Fuel rig", "Fuel system", "Gearbox", "Halfshaft",
        "Handling", "Heat shield fire", "Hydraulics", "Ignition", "Injection",
        "Magneto", "Mechanical", "Oil leak", "Oil line", "Oil pipe", "Oil pressure",
        "Oil pump", "Overheating", "Pneumatics", "Power Unit", "Power loss",
        "Radiator", "Spark plugs", "Steering", "Supercharger", "Suspension",
        "Throttle", "Track rod", "Transmission", "Turbo", "Vibrations",
        "Water leak", "Water pipe", "Water pressure", "Water pump", "Wheel bearing"
    ],

    "Accident / Collision": [
        "Accident", "Collision", "Collision damage", "Damage", "Debris",
        "Fatal accident", "Fire", "Spun off"
    ],

    "Car Damage": [
        "Broken wing", "Front wing", "Rear wing", "Undertray",
        "Puncture", "Tyre", "Tyre puncture",
        "Wheel", "Wheel nut", "Wheel rim"
    ],

    "Regulations / Technical": [
        "107% Rule", "Disqualified", "Excluded", "Launch control",
        "Not classified", "Safety", "Safety concerns", "Technical", "Underweight"
    ],

    "Strategic / Race": [
        "Out of fuel", "Refuelling", "Retired", "Stalled", "Withdrew"
    ]
}