import random
import time
import textwrap

#timeloop_concept
class TimeLoopAdventure:
    """
    Summit-inspired text adventure game."""

    POSITIVE = ("y", "yes")
    NEGATIVE = ("n", "no")

    def __init__(self) -> None:
        self.loop_count = 0
        self.intel = {
            "knows_signal_time": False,
            "knows_bag": False,
            "knows_route": False,
        }
        self.items = []
        self.used_choices = set()


    def cprint(self, message: str, delay: float = 1.0) -> None:
        print(message)
        time.sleep(delay)

    def cprint2(
        self,
        message: str,
        width: int = 60,
        delay: float = 0.6,
    ) -> None:
        for line in textwrap.wrap(message, width):
            print(line)
            time.sleep(delay)

    def divider(self) -> None:
        print("\n" + "*" * 60 + "\n")
        time.sleep(0.4)


    def get_yes_no(self, prompt: str) -> bool:
        while True:
            answer = input(prompt).strip().lower()
            if answer in self.POSITIVE:
                return True
            if answer in self.NEGATIVE:
                return False
            self.cprint("Invalid input. Please type yes/y or no/n.", 0.5)

    def get_menu_choice(self, prompt: str, valid: set[int]) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                choice = int(raw)
            except ValueError:
                self.cprint("Invalid input. Enter a number.", 0.5)
                continue

            if choice not in valid:
                self.cprint("That is not a valid option. Try again.", 0.5)
                continue

            return choice



    def reset_loop(self, reason: str) -> None:
        """
        Time-loop reset:
        - Increments loop count
        - Clears loop inventory + used menu choices
        - Keeps intel (memories)
        """
        self.loop_count += 1
        self.items = []
        self.used_choices = set()

        self.divider()
        self.cprint2(reason)
        self.cprint2(
            f"Time snaps back to the same morning... (Loop #{self.loop_count})"
        )
        self.cprint2("Your memories remain. Use what you learned.")
        self.divider()

        play_again = self.get_yes_no("Play again from the loop start? (y/n) ")
        if play_again:
            self.main_menu()
        else:
            self.cprint("You step away... but the day keeps repeating.", 1.0)
            self.end_game()

    def end_game(self) -> None:
        self.cprint("\nEnd of adventure.")
        raise SystemExit

    def win(self) -> None:
        self.divider()
        self.cprint2("The loop stops.")
        self.cprint2("For the first time... the next minute belongs to you.")
        self.cprint("\nYOU SAVED THE LEADER AND BROKE THE TIME LOOP!")
        self.divider()

        play_again = self.get_yes_no("Do you want to play again? (y/n) ")
        if play_again:
            self.fresh_start()
        else:
            self.end_game()

    def fresh_start(self) -> None:
        """
        Full restart:
        - Clears intel and starts from loop #0
        """
        self.loop_count = 0
        self.intel = {
            "knows_signal_time": False,
            "knows_bag": False,
            "knows_route": False,
        }
        self.items = []
        self.used_choices = set()
        self.intro()

    # ------------- Story / UI -------------
    def show_status(self) -> None:
        intel_bits = (
            f"signal_time={self.intel['knows_signal_time']}, "
            f"bag={self.intel['knows_bag']}, "
            f"route={self.intel['knows_route']}"
        )
        self.cprint(f"[Loop #{self.loop_count}] INTEL: {intel_bits}", 0.2)
        inv = ", ".join(self.items) if self.items else "empty"
        self.cprint(f"Inventory (resets each loop): {inv}\n", 0.2)

    def intro(self) -> None:
        self.divider()
        self.cprint2("MAANAADU: TIME LOOP ADVENTURE")
        self.cprint2(
            "You are trapped in a repeating day during a political rally."
        )
        self.cprint2(
            "A conspiracy will trigger an assassination unless you stop it."
        )
        self.cprint2("If you die, the day resets. But you remember clues.")
        self.divider()

        accept = self.get_yes_no("Do you accept to play? (y/n) ")
        if accept:
            self.main_menu()
        else:
            self.cprint("You refuse... but the loop continues without you.")
            self.end_game()



    def main_menu(self) -> None:
        while True:
            self.divider()
            self.cprint2(
                "Morning. The conference center is ahead. The rally starts "
                "soon."
            )
            self.cprint2(
                "Choose how to enter, gather help, and stop the conspiracy."
            )
            self.show_status()

            self.cprint("Choose your action:")
            self.cprint("1. MAIN GATE (needs a pass)")
            self.cprint("2. CROWD ADULT (unpredictable)")
            self.cprint("3. POLICE (random chance)")
            self.cprint("4. SERVICE ROUTE (sequence puzzle)")
            self.cprint("5. Quit")
            print()

            choice = self.get_menu_choice(
                "Make a choice (1-5): ",
                {1, 2, 3, 4, 5},
            )

            if choice == 5:
                self.end_game()

            if choice in self.used_choices:
                self.cprint(
                    "You already tried that option in this loop. "
                    "Try something else.",
                    0.8,
                )
                continue

            self.used_choices.add(choice)

            if choice == 1:
                self.main_gate()
            elif choice == 2:
                self.crowd_adult()
            elif choice == 3:
                self.police_help()
            elif choice == 4:
                self.service_route()



    def main_gate(self) -> None:
        self.divider()
        self.cprint2(
            "You approach the main gate. Guards check passes. Cameras watch."
        )

        if "pass" not in self.items:
            self.cprint2("A guard blocks you: 'Pass required.'")
            self.cprint2(
                "You may need help from the crowd, police, or another route."
            )
            return

        self.cprint2("You show your pass. The guard lets you enter.")
        self.inside_hub()

    def crowd_adult(self) -> None:
        self.divider()
        self.cprint2(
            "You move into the crowd outside. People chant and push."
        )

        gender = random.choice(["male", "female"])

        if gender == "male":
            self.cprint2("A busy man looks irritated and in a hurry.")
            talk = self.get_yes_no("Do you want to talk to him? (y/n) ")
            if not talk:
                self.cprint2("You step away and scan the crowd.")
                self.crowd_search()
                return

            aggression = random.randint(1, 10)
            if aggression >= 6:
                self.reset_loop(
                    "He shoves you. You hit your head in the chaos."
                )
                return

            self.cprint2("He calms down and whispers: 'Signal at 12:10.'")
            self.intel["knows_signal_time"] = True
            self.cprint2("He slips you a staff pass he found on the ground.")
            if "pass" not in self.items:
                self.items.append("pass")
            return

        self.cprint2("A woman notices your panic and helps you breathe.")
        self.cprint2("She points: 'Two men carried a suspicious bag backstage.'")
        self.intel["knows_bag"] = True
        self.cprint2("She hands you an entry token that works like a pass.")
        if "pass" not in self.items:
            self.items.append("pass")

    def crowd_search(self) -> None:
        while True:
            self.cprint("\nIn the crowd you can:")
            self.cprint("1. Follow the suspicious men")
            self.cprint("2. Go to a tea stall to overhear secrets")
            self.cprint("3. Return to main choices")
            print()

            choice = self.get_menu_choice(
                "Choose 1/2/3: ",
                {1, 2, 3},
            )
            if choice == 1:
                self.follow_men()
                return
            if choice == 2:
                self.tea_stall()
                return
            if choice == 3:
                return

    def tea_stall(self) -> None:
        self.divider()
        self.cprint2(
            "You stop at a tea stall. People talk when they feel safe."
        )

        roll = random.randint(1, 10)

        if roll >= 7 and not self.intel["knows_signal_time"]:
            self.cprint2("You overhear: 'At exactly 12:10, send the signal.'")
            self.intel["knows_signal_time"] = True
            return

        if roll >= 5 and "pass" not in self.items:
            self.cprint2("You spot a staff pass under a chair and take it.")
            self.items.append("pass")
            return

        self.cprint2("You learn nothing solid, but you feel the tension grow.")

    def follow_men(self) -> None:
        self.divider()
        self.cprint2("You follow two men weaving through the crowd.")

        if not self.intel["knows_route"]:
            self.cprint2(
                "You glimpse the route: Right → Left → Straight → Door."
            )
            self.intel["knows_route"] = True

        spotted = random.randint(1, 10) < 6
        if spotted:
            self.reset_loop("One of them notices you and attacks.")
        else:
            self.cprint2("You dodge into the crowd and escape with new intel.")

    def police_help(self) -> None:
        self.divider()
        self.cprint2("You approach the police near their vehicle.")

        availability = random.randint(1, 10)
        bonus = 0
        if self.intel["knows_signal_time"]:
            bonus += 2
        if self.intel["knows_bag"]:
            bonus += 2

        if availability + bonus >= 9:
            self.cprint2(
                "The officer believes you. He gives you a radio and escort."
            )
            if "radio" not in self.items:
                self.items.append("radio")
            if "pass" not in self.items:
                self.items.append("pass")
            self.inside_hub()
        else:
            self.cprint2("The officer dismisses you: 'No panic here.'")

    def service_route(self) -> None:
        self.divider()
        self.cprint2(
            "You slip toward the service route: narrow halls and staff doors."
        )
        self.cprint2(
            "To reach backstage, enter the correct direction sequence."
        )
        self.cprint("1. Left  2. Right  3. Straight  4. Door\n")

        correct = [2, 1, 3, 4]  
        attempt = []

        while len(attempt) < 4:
            step = self.get_menu_choice(
                f"Step {len(attempt) + 1} (1-4): ",
                {1, 2, 3, 4},
            )
            attempt.append(step)

        if self.intel["knows_route"]:
            mistakes = sum(
                1 for a, b in zip(attempt, correct) if a != b
            )
            if mistakes <= 1:
                self.cprint2("Your memory guides you. You reach backstage!")
                self.backstage()
                return

        if attempt == correct:
            self.cprint2("Perfect. You reach backstage!")
            self.backstage()
            return

        self.reset_loop("Wrong turn. A guard spots you and shoots.")



    def inside_hub(self) -> None:
        while True:
            self.divider()
            self.cprint2("You are inside the conference center.")
            self.cprint2("Choose where to go next.")
            self.show_status()

            self.cprint("1. Stage Control (stop the signal)")
            self.cprint("2. Backstage (look for the bag)")
            self.cprint("3. Search Hall (find evidence)")
            self.cprint("4. Return outside")
            print()

            choice = self.get_menu_choice("Choose 1-4: ", {1, 2, 3, 4})

            if choice == 1:
                self.stage_control()
                return
            if choice == 2:
                self.backstage()
                return
            if choice == 3:
                self.search_hall()
                return
            if choice == 4:
                return



    def search_hall(self) -> None:
        self.divider()
        self.cprint2("You search the hall. Staff rush around. Phones buzz.")

        if "radio" in self.items:
            self.cprint2("Your radio picks up: 'Bag near backstage exit!'")
            self.intel["knows_bag"] = True
        else:
            self.cprint2("You find a torn note: 'Signal @ 12:10'.")
            self.intel["knows_signal_time"] = True

        self.cprint2("You head back.")



    def backstage(self) -> None:
        self.divider()
        self.cprint2("Backstage is tense. Guards watch the curtains.")

        if not self.intel["knows_bag"]:
            self.reset_loop(
                "You waste time searching blindly. A shot rings out."
            )
            return

        self.cprint2("You spot the suspicious bag behind stacked banners.")
        self.cprint2("You must act fast.")
        print()

        self.cprint("1. Defuse the device (wire puzzle)")
        self.cprint("2. Call police (needs radio)")
        self.cprint("3. Throw it away (dangerous)")
        print()

        choice = self.get_menu_choice("Choose 1-3: ", {1, 2, 3})

        if choice == 1:
            self.defuse_puzzle()
            return

        if choice == 2:
            if "radio" in self.items:
                self.cprint2("Police rush in and secure the device.")
                self.final_confrontation()
            else:
                self.reset_loop("No radio. You shout for help. Too late.")
            return

        self.reset_loop("You grab the bag to throw it away... it explodes.")



    def defuse_puzzle(self) -> None:
        self.divider()
        self.cprint2("Defuse puzzle: cut 3 wires. Do NOT cut black.")
        self.cprint("Wires: red, blue, yellow, black\n")

        valid = {"red", "blue", "yellow", "black"}
        good1 = ["blue", "yellow", "red"]
        good2 = ["yellow", "blue", "red"]

        sequence = []
        while len(sequence) < 3:
            wire = input(f"Cut wire {len(sequence) + 1}: ").strip().lower()
            if wire not in valid:
                self.cprint("Invalid wire. Try again.", 0.5)
                continue
            if wire == "black":
                self.reset_loop("You cut black. Instant explosion.")
                return
            sequence.append(wire)

        if sequence == good1 or sequence == good2:
            self.cprint2("The timer dies. You did it!")
            self.final_confrontation()
        else:
            self.reset_loop("Wrong order. The device detonates.")



    def stage_control(self) -> None:
        self.divider()
        self.cprint2("Stage Control is full of cables, switches, and screens.")

        if not self.intel["knows_signal_time"]:
            self.reset_loop(
                "You don't know the timing. A guard shoots you for tampering."
            )
            return

        self.cprint2("You remember: the signal triggers at 12:10.")
        self.cprint2("To jam it, choose the correct switch sequence.")
        self.cprint("1. Power  2. Jammer  3. Confirm\n")

        correct = [1, 2, 3]
        attempt = []

        while len(attempt) < 3:
            step = self.get_menu_choice(
                f"Step {len(attempt) + 1} (1-3): ",
                {1, 2, 3},
            )
            attempt.append(step)

        if attempt == correct:
            self.cprint2("Signal jammed! The plot is disrupted.")
            self.final_confrontation()
        else:
            self.reset_loop("Wrong switch order. Sparks fly. Everything fades.")



    def final_confrontation(self) -> None:
        self.divider()
        self.cprint2("A runner tries to escape through the exit.")
        self.cprint2("This is your chance to end the loop.")

        score = 0
        score += 2 if self.intel["knows_signal_time"] else 0
        score += 2 if self.intel["knows_bag"] else 0
        score += 1 if self.intel["knows_route"] else 0
        score += 2 if "radio" in self.items else 0

        self.cprint("\nChoose your move:")
        self.cprint("1. Capture him (fight; random)")
        self.cprint("2. Record confession (best with radio)")
        self.cprint("3. Drag him to police (needs radio)")
        print()

        choice = self.get_menu_choice("Choose 1-3: ", {1, 2, 3})

        if choice == 1:
            roll = random.randint(1, 10) + score
            if roll >= 10:
                self.cprint2("You tackle him and grab his phone: evidence!")
                self.win()
            else:
                self.reset_loop("He stabs you and vanishes into the crowd.")
            return

        if choice == 2:
            if "radio" in self.items or score >= 6:
                self.cprint2("You record the confession and broadcast it.")
                self.win()
            else:
                self.reset_loop("No signal, no proof. He escapes. You're shot.")
            return

        if "radio" in self.items:
            self.cprint2("Police witness everything and arrest the conspirators.")
            self.win()
        else:
            self.reset_loop("You can't reach police in time. The runner escapes.")



    def start(self) -> None:
        self.fresh_start()


def main() -> None:
    game = TimeLoopAdventure()
    game.start()


if __name__ == "__main__":
    main()
