import random
import time
import textwrap


loop_count = 0

choices = [1, 2, 3, 4]
choices_copy = choices.copy()

positive = ["yes", "y"]
negative = ["no", "n"]

intel = {
    "knows_signal_time": False,
    "knows_bag": False,
    "knows_route": False,
}

items = []




def cprint(message, delay=1):
    print(message)
    time.sleep(delay)


def cprint2(message, width=60, delay=0.6):
    wrapped = textwrap.wrap(message, width)
    for line in wrapped:
        print(line)
        time.sleep(delay)


def divider():
    print("\n" + "*" * 60 + "\n")
    time.sleep(0.4)




def get_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in positive:
            return True
        if answer in negative:
            return False
        cprint("Invalid input. Please type yes/y or no/n.", 0.5)


def get_choice_int(prompt, valid_choices):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            cprint("Invalid input. Enter a number.", 0.5)
            continue

        if value not in valid_choices:
            cprint("That's not an option. Try again.", 0.5)
            continue

        return value


def reset_loop(reason="You died."):
    """Resets loop-specific stuff, keeps intel."""
    global loop_count, choices, items

    loop_count += 1
    choices = choices_copy.copy()
    items = []

    divider()
    cprint2(reason)
    cprint2(
        f"Time snaps back to the SAME morning... (Loop #{loop_count})"
    )
    cprint2("But your memories remain. Use what you learned.")
    divider()

    play_again = get_yes_no("Do you want to play again? (y/n) ")
    if play_again:
        play()
    else:
        end_game()


def end_game():
    cprint("\nEnd of adventure.")
    raise SystemExit


def win():
    divider()
    cprint2("The loop stops.")
    cprint2("For the first time... the next minute belongs to you.")
    cprint("YOU SAVED THE LEADER AND BROKE THE TIME LOOP!")
    divider()

    play_again = get_yes_no("Do you want to play again? (y/n) ")
    if play_again:
        full_restart()
    else:
        end_game()


def full_restart():
    """Restart everything, including intel."""
    global loop_count, choices, items

    loop_count = 0
    choices = choices_copy.copy()
    items = []

    intel["knows_signal_time"] = False
    intel["knows_bag"] = False
    intel["knows_route"] = False

    intro()


def show_status():
    cprint(
        "[Loop #{0}] INTEL: signal_time={1}, bag={2}, route={3}".format(
            loop_count,
            intel["knows_signal_time"],
            intel["knows_bag"],
            intel["knows_route"],
        ),
        0.2,
    )
    inv = items if items else "empty"
    cprint(f"Inventory (resets each loop): {inv}\n", 0.2)


#Intro to Story
def intro():
    divider()
    cprint2("MAANAADU: TIME LOOP ADVENTURE")
    cprint2("You are trapped in a repeating day during a political rally.")
    cprint2("A conspiracy will trigger an assassination unless you stop it.")
    cprint2("If you die... the day resets. But you remember clues.")
    divider()

    accept = get_yes_no("Do you accept to play? (yes/no) ")
    if accept:
        play()
    else:
        cprint("You refuse... but the loop continues without you.")
        end_game()


#Main
def play():
    global choices

    while True:
        divider()
        cprint2(
            "Morning. The conference center is ahead. The rally starts soon."
        )
        cprint2("You must choose how to enter and gather help.")
        show_status()

        cprint("Choose your action:")
        cprint("1. Go through the MAIN GATE (security checkpoint)")
        cprint("2. Ask a CROWD ADULT for help (unpredictable)")
        cprint("3. Ask the POLICE for help (random chance)")
        cprint("4. Take the SERVICE ROUTE (risky, puzzle)")
        cprint("5. Quit")
        print()

        choice = get_choice_int("Make a choice: ", {1, 2, 3, 4, 5})

        if choice == 5:
            end_game()

        if choice not in choices:
            cprint(
                "You already tried this option in this loop. "
                "Try other options.",
                0.8,
            )
            continue

        choices.remove(choice)

        if choice == 1:
            main_gate()
        elif choice == 2:
            crowd_adult()
        elif choice == 3:
            police_help()
        elif choice == 4:
            service_route()

        # After returning from branch printing loop main menu again.


#Location
def main_gate():
    divider()
    cprint2("You approach the MAIN GATE. Guards check passes. Cameras watch.")
    cprint2(
        "You notice three paths inside: Control Room, Backstage, Crowd Hall."
    )
    cprint("")

    if "pass" not in items:
        cprint2("A guard blocks you: 'Pass required.'")
        cprint2("Maybe you can find a pass or some proof elsewhere.")
        return

    cprint2("You show your PASS. The guard lets you enter.")
    inside_hub()


def crowd_adult():
    divider()
    cprint2("You move into the crowd outside. People chant and push.")

    gender = random.choice(["male", "female"])

    if gender == "male":
        cprint2("You approach a busy man. He looks irritated.")
        talk = get_yes_no("Do you want to talk to him? (y/n) ")
        if not talk:
            cprint2("You step away and scan the crowd...")
            crowd_search()
            return

        agg = random.randint(1, 10)
        if agg >= 6:
            cprint2("He snaps: 'Move!' and shoves you.")
            cprint2("You stumble into a barricade...")
            reset_loop("You hit your head hard.")
            return

        cprint2("He listens. He whispers: 'The signal goes at 12:10.'")
        intel["knows_signal_time"] = True
        cprint2("He slips you a STAFF PASS he found on the ground.")
        if "pass" not in items:
            items.append("pass")
        return

    cprint2("A woman sees your panic and helps you calm down.")
    cprint2("She points: 'Two men carried a suspicious bag backstage.'")
    intel["knows_bag"] = True
    cprint2("She hands you a small ENTRY TOKEN. It might work as a pass.")
    if "pass" not in items:
        items.append("pass")


def crowd_search():
    """Small exploration like passageways - get items or risk trouble."""
    while True:
        cprint("\nIn the crowd you can:")
        cprint("1. Follow the suspicious men")
        cprint("2. Go to a tea stall to overhear secrets")
        cprint("3. Return to the main choices")
        print()

        sub = get_choice_int("Choose 1/2/3: ", {1, 2, 3})

        if sub == 1:
            follow_men()
            return
        if sub == 2:
            tea_stall()
            return
        if sub == 3:
            return


def tea_stall():
    divider()
    cprint2(
        "You stop at a tea stall. People talk when nobody seems to listen."
    )
    roll = random.randint(1, 10)

    if roll >= 7 and not intel["knows_signal_time"]:
        cprint2("You overhear: 'At exactly 12:10, send the signal.'")
        intel["knows_signal_time"] = True
    elif roll >= 5 and "pass" not in items:
        cprint2("You spot a STAFF PASS under a chair and quietly take it.")
        items.append("pass")
    else:
        cprint2("You hear rumors but nothing solid.")

    cprint2("You head back.")


def follow_men():
    divider()
    cprint2("You follow the men weaving through the crowd.")

    if not intel["knows_route"]:
        cprint2("You glimpse the route: Right → Left → Straight → Door.")
        intel["knows_route"] = True

    cprint2("One of them notices you...")
    roll = random.randint(1, 10)
    if roll >= 6:
        cprint2("You dodge into the crowd and escape.")
        cprint2("You gained useful intel.")
        return

    reset_loop("They stab you in the chaos.")


def police_help():
    divider()
    cprint2("You approach the POLICE near their vehicle.")
    availability = random.randint(1, 10)

    bonus = 0
    if intel["knows_signal_time"]:
        bonus += 2
    if intel["knows_bag"]:
        bonus += 2

    if availability + bonus >= 9:
        cprint2(
            "The officer believes you. He gives you a RADIO and escorts you "
            "inside."
        )
        if "radio" not in items:
            items.append("radio")
        if "pass" not in items:
            items.append("pass")
        inside_hub()
        return

    cprint2("The officer dismisses you. 'No panic here.'")


def service_route():
    divider()
    cprint2("You slip toward the SERVICE ROUTE: narrow halls and staff doors.")
    cprint2("To reach backstage, choose the correct direction sequence.")
    cprint("1. Left  2. Right  3. Straight  4. Door\n")

    correct_seq = [2, 1, 3, 4]
    seq = []

    while len(seq) < 4:
        step = get_choice_int(f"Step {len(seq) + 1}: ", {1, 2, 3, 4})
        seq.append(step)

    if intel["knows_route"]:
        mistakes = sum(1 for a, b in zip(seq, correct_seq) if a != b)
        if mistakes <= 1:
            cprint2("Your memory guides you. You reach backstage!")
            backstage()
            return

    if seq == correct_seq:
        cprint2("You reach backstage!")
        backstage()
        return

    reset_loop("Wrong turn. A guard shoots you in the corridor.")


#Final_step
def inside_hub():
    while True:
        divider()
        cprint2("You are inside the conference center.")
        cprint2("You can head to: Stage Control, Backstage, or Search Hall.")
        show_status()

        cprint("1. Go to STAGE CONTROL (stop the signal)")
        cprint("2. Go BACKSTAGE (look for bag)")
        cprint("3. Search HALL for evidence")
        cprint("4. Return outside")
        print()

        sub = get_choice_int("Choose 1/2/3/4: ", {1, 2, 3, 4})

        if sub == 1:
            stage_control()
            return
        if sub == 2:
            backstage()
            return
        if sub == 3:
            search_hall()
        if sub == 4:
            return


def search_hall():
    divider()
    cprint2("You search the hall. Staff rush around. Phones buzz.")

    if "radio" in items:
        cprint2("Your radio picks up: 'Bag is near backstage exit!'")
        intel["knows_bag"] = True
    else:
        cprint2("You find a torn note: 'Signal @ 12:10'.")
        intel["knows_signal_time"] = True

    cprint2("You head back.")


def backstage():
    while True:
        divider()
        cprint2("Backstage is tense. Guards watch the curtains.")

        if not intel["knows_bag"]:
            cprint2("You don't know what you're searching for.")
            cprint2("You waste time... and the assassination happens.")
            reset_loop("A shot rings out.")
            return

        cprint2("You spot the suspicious BAG behind stacked banners.")
        cprint2("You must act fast.")
        print()

        cprint("1. Defuse the device (wire puzzle)")
        cprint("2. Call police (needs radio)")
        cprint("3. Throw it away (dangerous)")
        print()

        sub = get_choice_int("Choose 1/2/3: ", {1, 2, 3})

        if sub == 1:
            defuse_puzzle()
            return

        if sub == 2:
            if "radio" in items:
                cprint2("Police rush in and secure the device.")
                final_choice()
                return
            reset_loop("No radio. You scream for help. Too late.")
            return

        reset_loop("You grab it—BOOM.")
        return


def defuse_puzzle():
    divider()
    cprint2("Defuse puzzle: cut 3 wires. Do NOT cut black.")
    cprint("Wires: red, blue, yellow, black\n")

    order1 = ["blue", "yellow", "red"]
    order2 = ["yellow", "blue", "red"]
    seq = []

    valid_wires = {"red", "blue", "yellow", "black"}

    while len(seq) < 3:
        wire = input(f"Cut wire {len(seq) + 1}: ").strip().lower()

        if wire not in valid_wires:
            cprint("Invalid wire. Try again.", 0.5)
            continue

        if wire == "black":
            reset_loop("You cut black. Instant explosion.")
            return

        seq.append(wire)

    if seq == order1 or seq == order2:
        cprint2("The timer dies. You did it!")
        final_choice()
        return

    reset_loop("Wrong order. The bomb detonates.")


def stage_control():
    divider()
    cprint2("Stage Control is full of cables and switches.")

    if not intel["knows_signal_time"]:
        cprint2("You don't know the timing. You press the wrong control...")
        reset_loop("A guard shoots you for tampering.")
        return

    cprint2("You remember: 12:10 signal trigger.")
    cprint2("To jam it, choose the correct switch sequence:")
    cprint("1. Power  2. Jammer  3. Confirm\n")

    correct = [1, 2, 3]
    seq = []

    while len(seq) < 3:
        pick = get_choice_int(f"Step {len(seq) + 1}: ", {1, 2, 3})
        seq.append(pick)

    if seq == correct:
        cprint2("Signal jammed! The plot is disrupted.")
        final_choice()
        return

    reset_loop("Wrong switch. Sparks fly. You collapse.")


def final_choice():
    while True:
        divider()
        cprint2("The mastermind's runner tries to escape through the exit.")
        cprint2("This is your chance to end the loop.")
        print()

        cprint("1. Capture him (fight - random)")
        cprint("2. Record confession (better if you have radio)")
        cprint("3. Drag him to police (better if you have radio)")
        print()

        final = get_choice_int("Choose 1/2/3: ", {1, 2, 3})

        score = 0
        score += 2 if intel["knows_signal_time"] else 0
        score += 2 if intel["knows_bag"] else 0
        score += 1 if intel["knows_route"] else 0
        score += 2 if "radio" in items else 0

        if final == 1:
            if random.randint(1, 10) + score >= 10:
                cprint2("You tackle him and grab his phone—evidence!")
                win()
            else:
                reset_loop("He stabs you and disappears into the crowd.")
            return

        if final == 2:
            if "radio" in items or score >= 6:
                cprint2("You record his confession and broadcast it.")
                win()
            else:
                reset_loop("No proof, no signal. He escapes. You're shot.")
            return

        if final == 3:
            if "radio" in items:
                cprint2("Police witness everything and arrest the conspirators.")
                win()
            else:
                reset_loop("You can't reach police in time. Runner escapes.")
            return


def start():
    global loop_count, choices, items
    loop_count = 0
    choices = choices_copy.copy()
    items = []
    intro()


if __name__ == "__main__":
    start()
