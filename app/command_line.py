from app.controller import Controller


class CommandLine:
    """
    Class to that creates the interaction layer for a user with this application

    Use start() to start the application
    """

    def __init__(self, controller: Controller):
        """
        Initializer for a CommandLine object

        :param controller: Controller object for this application
        """
        self.controller = controller
        self.intersection = controller.intersection

    def start(self) -> None:
        """
        Starts this application.

        Is the entry point into this application

        :return: None
        """
        if CommandLine.__wants_to_start():
            self.setup()
            self.__cycle_manual()
        self.__exit()

    def setup(self) -> None:
        """
        Handles setting up this application, after a user has indicated that they would like to start

        :return: None
        """
        self.controller.should_wait = self.wants_to_wait()
        #self.wants_auto = self.__wants_to_automate()

    def __wants_to_automate(self) -> bool:
        """
        Asks a user if they want to automate the running of the application or not

        Essentially boils down to not asking user if they would like to continue to the next cycle each time
        a cycle has finished

        :return: bool, True if they would like to automate, otherwise False
        """
        return self.__enter_yes_or_no("Would you like to automate Traffic controller")

    def wants_to_wait(self) -> bool:
        """
        Handles asking a user if they would like to wait in real time for each cycle to finish or not, or just
        complete cycles instantaneously

        :return: bool, True if they would like to wait, otherwise False
        """
        return self.__enter_yes_or_no("Would you like to sleep this application in real time to reflect time for "
                                      "traffic to clear the intersection")


    def __display_state(self) -> None:
        """
        Displays the state of this application. So a user can track progress and monitor performance

        :return: None
        """
        avg_waiting_time = self.intersection.avg_waiting_time
        num_vehicles = self.intersection.num_vehicles
        msg = "The intersection has {} vehicles with an average waiting time of {:.2f}" \
            .format(num_vehicles, avg_waiting_time)
        print(msg)

    def __cycle_auto(self) -> None:
        self.__display_state()
        self.controller.cycle()
        #self.cy
        pass

    def __cycle_manual(self) -> None:
        """
        Manually cycles through each direction for the intersection being managed, stops cycling if user asks so

        :return: None
        """
        self.__display_state()
        msg = "Would you like to continue to next cycle or exit"
        wants_to_continue = self.__enter_yes_or_no(msg)
        while wants_to_continue:
            self.controller.cycle()
            self.__display_state()
            wants_to_continue = self.__enter_yes_or_no(msg)
        CommandLine.__exit()

    @staticmethod
    def __exit() -> None:
        """
        Handles the exiting of this application

        :return: None
        """
        print("Thanks for using TrafficController, bye!")

    @staticmethod
    def __enter_yes_or_no(msg: str) -> bool:
        """
        Handles asking a user an answer to a yes or no question.

        Keeps asking them for input until either 'Y' or 'N' is entered

        :param msg: str for the question to be asked of a user to that needs a yes or no answer
        :return: bool, True if user enters Yes or False if user enters No
        """
        print("{}? (Y/N)".format(msg))
        ans = input()
        while ans not in ["Y", "N"]:
            print("Answer must be either 'Y' or 'N'!")
            ans = input()
        return ans == "Y"

    @staticmethod
    def __wants_to_start() -> bool:
        """
        Welcomes a user to the application and asks if they would like to start or not

        :return: bool if a user would like to start the application or not
        """
        print("Hello and welcome to TrafficController")
        return CommandLine.__enter_yes_or_no("Would you like to start")
