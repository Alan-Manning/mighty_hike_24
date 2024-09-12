import sys
from datetime import datetime
from enum import IntEnum
from typing import Any, Callable, Sequence

import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup
from matplotlib.axes import Axes
from matplotlib.ticker import FuncFormatter


class MightHikeLocation(IntEnum):
    """All of the Might Hike locations.

    Members
    -------
    Wye_Valley = 20439
    Jurassic_Coast = 20440
    Rob_Roy = 20437
    Cornwall_Coast = 20438
    Peak_District = 20436
    Thames_Path = 20435
    Gower_Peninsula = 20434
    Yorkshire_Dales = 20433
    Giants_Causeway = 20432
    Lake_District = 20431
    South_Coast = 20430
    London = 20429
    Eryri_Snowdonia = 20428
    Norfolk_Coast = 20427
    """

    Wye_Valley = 20439
    Jurassic_Coast = 20440
    Rob_Roy = 20437
    Cornwall_Coast = 20438
    Peak_District = 20436
    Thames_Path = 20435
    Gower_Peninsula = 20434
    Yorkshire_Dales = 20433
    Giants_Causeway = 20432
    Lake_District = 20431
    South_Coast = 20430
    London = 20429
    Eryri_Snowdonia = 20428
    Norfolk_Coast = 20427


def seconds_to_human_time(seconds: int) -> str:
    """Convert number of seconds to str of human readable time.
    Will return H:MM:SS if the time spans into the hours. It will return MM:SS
    if it only extends into the Mins. If it is not long enough still it will
    just show SS seconds with a "s" after to show this in a nicer format.

    Parameters
    ----------
    seconds: int
        A number of seconds to convert.

    Returns
    -------
    time_string: str
        The human readable time as a string.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours != 0:
        return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    if minutes != 0:
        return "{:2d}:{:02d}".format(minutes, seconds)
    return "{:2d}s".format(seconds)


class Person:
    """Takes in a persons name, race number and times and has helper methods
    to get information about the persons times.

    Parameters
    ----------
    name: str
        The persons name.

    race_number: int
        The persons race number.

    start: str,
        The start time as a string.

    pitstop_1: str,
        The time the person reached pitstop 1 as a string.

    pitstop_2: str,
        The time the person reached pitstop 2 as a string.

    pitstop_3: str,
        The time the person reached pitstop 3 as a string.

    finish: str,
        The time the person finished as a string.

    KwArgs
    ------
    time_format: str = "%H:%M:%S",
        This is the time format for each of the times given above. The default
        is Hours:Mins:Seconds seperated by `:` characters. This is the format
        given by the official results page.
    """

    def __init__(
        self,
        name: str,
        race_number: int,
        start: str,
        pitstop_1: str,
        pitstop_2: str,
        pitstop_3: str,
        finish: str,
        time_format: str = "%H:%M:%S",
    ):
        self.name = name
        self.first_name = name.split(" ")[0]
        self.race_number = race_number
        self.start = datetime.strptime(start, time_format)
        self.pitstop_1 = datetime.strptime(pitstop_1, time_format)
        self.pitstop_2 = datetime.strptime(pitstop_2, time_format)
        self.pitstop_3 = datetime.strptime(pitstop_3, time_format)
        self.finish = datetime.strptime(finish, time_format)

    def __str__(self) -> str:
        """."""
        string = "Person:\n"
        string += f"    Race No : {self.race_number}\n"
        string += f"       name : {self.name}\n"
        string += f"       start: {self.start}\n"
        string += f"   pitstop_1: {self.pitstop_1}\n"
        string += f"   pitstop_2: {self.pitstop_2}\n"
        string += f"   pitstop_3: {self.pitstop_3}\n"
        string += f"     finish : {self.finish}\n"
        return string

    def get_leg_time(self, leg_no: int) -> int:
        """Get the time for a specified leg number in seconds."""
        match leg_no:
            case 1:
                time = self.pitstop_1 - self.start
                return time.seconds
            case 2:
                time = self.pitstop_2 - self.pitstop_1
                return time.seconds
            case 3:
                time = self.pitstop_3 - self.pitstop_2
                return time.seconds
            case 4:
                time = self.finish - self.pitstop_3
                return time.seconds
            case _:
                raise ValueError(f"leg_no out of bounds 1->4 inclusive.")

    @property
    def total_time(self) -> int:
        """The total time in seconds."""
        time = self.finish - self.start
        return time.seconds


class People:
    """A collection of People objects which handles plotting each persons
    times to a figure.

    Parameters
    ----------
    people: Sequence[Person]
        A list type of Person objects to have managed for plotting.

    KwArgs
    ------
    time_fmt_func: Callable | None = None
        This is an optional time formatting function. This function should
        take in a time in seconds and return a string of the formatted time.
        When this is not defined the time formatting will be done by the
        seconds_to_hours_mins() method. See this method for more info on
        generating an Callable override.
    """

    def __init__(
        self,
        people: Sequence[Person],
        time_fmt_func: Callable[[int], str] | None = None,
    ):

        self.people = people
        self.people.sort(key=lambda p: p.total_time)

        set_of_names = set(person.name for person in self.people)
        if len(set_of_names) == len(self.people):
            self.use_first_name_in_plots = True
        else:
            self.use_first_name_in_plots = False

        if time_fmt_func is None:
            self.time_formatter = FuncFormatter(self.seconds_to_hours_mins)
        else:
            self.time_formatter = FuncFormatter(time_fmt_func)

    def seconds_to_hours_mins(self, secs: int) -> str:
        """Convert seconds to H:MM format."""
        hours = int(secs // 3600)
        minutes = int((secs % 3600) // 60)
        return "{:d}:{:02d}".format(hours, minutes)

    def plot_leg_as_bar(self, ax: Axes, leg_no: int) -> None:
        """Plot a bar for each person for a specified leg number on the xaxis
        with time on the yaxis and format it.

        Parameters
        ----------
        ax: Axes
            The figure axes to plot the leg time chart to.

        leg_no: int
            The leg number to plot. This is an int value of either:
            `1`, `2`, `3` or `4`.
        """
        times = []
        for person in self.people:
            time = person.get_leg_time(leg_no)
            times.append(time)
            name = person.first_name if self.use_first_name_in_plots else person.name
            ax.bar(name, time, alpha=0.8)

        for i, person in enumerate(self.people):
            time = person.get_leg_time(leg_no)
            ax.text(
                i,
                time,
                seconds_to_human_time(time),
                rotation=-90,
                horizontalalignment="center",
                verticalalignment="top",
            )
            if time == min(times):
                continue
            ax.text(
                i,
                time,
                f"+{seconds_to_human_time(time - min(times))}",
                horizontalalignment="center",
                verticalalignment="bottom",
            )

        ax.set_ylim(min(times) * 0.965, max(times) * 1.009)
        ax.get_ylim()
        ax.yaxis.set_ticks(np.linspace(*ax.get_ylim(), 15))
        ax.yaxis.set_major_formatter(self.time_formatter)
        for tick in ax.get_xticklabels():
            tick.set_rotation(-70)

        ax.set_title(f"Leg {leg_no}")
        ax.grid(alpha=0.3)

    def plot_total_as_bar(self, ax: Axes) -> None:
        """Plot a bar for each person for the total time on the xaxis
        with person on the yaxis and format it.

        Parameters
        ----------
        ax: Axes
            The figure axes to plot the total time chart to.
        """
        times = []
        for i, person in enumerate(self.people):
            time = person.total_time
            times.append(time)
            name = person.first_name if self.use_first_name_in_plots else person.name
            ax.barh(name, time, alpha=0.8, color=f"C{i}")

        for i, person in enumerate(self.people):
            time = person.total_time
            ax.text(
                time,
                i,
                seconds_to_human_time(time),
                horizontalalignment="right",
                verticalalignment="center",
            )
            if time == min(times):
                continue
            ax.text(
                time * 1.0005,
                i,
                f"+{seconds_to_human_time(time - min(times))}",
                # rotation=-90,
                horizontalalignment="left",
                verticalalignment="center",
            )

        ax.set_xlim(min(times) * 0.99, max(times) * 1.005)
        ax.get_xlim()
        ax.xaxis.set_ticks(np.linspace(*ax.get_xlim(), 15))
        ax.xaxis.set_major_formatter(self.time_formatter)

        ax.set_title(f"Total Time")
        ax.set_xlabel("Time     (Hours : Mins)")
        ax.grid(alpha=0.3)

    def plot(self) -> None:
        """Plot the data for each of the 4 Legs and the overall."""
        title = "Mighty_Hike"
        fig = plt.figure(title, figsize=(16, 9))
        plt.clf()
        rows = 2
        cols = 4
        grid = plt.GridSpec(
            rows,
            cols,
            top=0.95,
            bottom=0.05,
            left=0.05,
            right=0.99,
            hspace=0.19,
            wspace=0.25,
        )

        axs: list[list[Axes]] = []

        for row in range(1):
            ax_row = []
            for col in range(cols):
                ax_row.append(plt.subplot(grid[row, col]))
            axs.append(ax_row)

        ax_row = []
        ax_row.append(plt.subplot(grid[1, 0:cols]))
        axs.append(ax_row)

        for leg_no in range(1, 4 + 1):
            ax = axs[0][leg_no - 1]
            self.plot_leg_as_bar(ax, leg_no)
        axs[0][0].set_ylabel("Time     (Hours : Mins)")

        self.plot_total_as_bar(axs[1][0])

        fig.savefig(f"MightHike_2024_plot")
        print("Saved plot as MightHike_2024_plot.png")
        fig.show()


def generate_person_from_race_nubmer(
    race_location: MightHikeLocation,
    race_number: int,
) -> Person:
    """Generate a Person object from a race number looking up relevant times
    from online.

    Parameters
    ----------
    race_location: MightHikeLocation
        The location of the Mighty Hike.

    race_number: int
        The race number of the person to add.

    Returns
    -------
    person: Person
        The Person object generated.
    """

    base_url = "https://results.resultsbase.net/"

    search_results_page_url = (
        base_url + f"Search.aspx?CId=8&RId={race_location.value}&S={race_number}"
    )

    try:
        #######################################################################
        search_results_page = requests.get(search_results_page_url)
        search_results_soup = BeautifulSoup(search_results_page.content, "html.parser")

        result = search_results_soup.find(
            "table", {"id": "ctl00_Content_Main_grdSearch"}
        )

        person_name = result.find_all("a")[0].get_text()
        href_to_stats_page = result.find_all("a", href=True)[0]["href"]

        stats_page_url = base_url + href_to_stats_page

        #######################################################################
        stats_page_result = requests.get(stats_page_url)
        stats_page_soup = BeautifulSoup(stats_page_result.content, "html.parser")

        result = stats_page_soup.find("div", {"id": "ctl00_Content_Main_divSplitGrid"})
        table = result.find("table")
        stats_table_rows = table.find_all("tr")[1:]

        data_dict: dict[str, Any] = {}

        data_dict["name"] = person_name
        data_dict["race_number"] = race_number

        for row_number, table_row in enumerate(stats_table_rows):
            table_datas = table_row.find_all("td")[:2]
            key = str(table_datas[0].get_text())
            key = key.lower()
            key = key.replace(" ", "_")
            val = str(table_datas[1].get_text())
            data_dict[key] = val

        person = Person(**data_dict)
        print(
            f"Succesfully parsed data for race number `{race_number}` -> {person_name}."
        )
        return person

    except Exception as e:
        raise RuntimeError(
            f"Could not find relevant data for race_number {race_number}."
        )


def generate_people_from_race_nubmers(
    race_location: MightHikeLocation,
    race_numbers: Sequence[int],
) -> People:
    """Generate a Person object from a race number looking up relevant times
    from online.

    Parameters
    ----------
    race_location: MightHikeLocation
        The location of the Mighty Hike.

    race_number: int
        The race number of the person to add.

    Returns
    -------
    person: Person
        The Person object generated.
    """

    people_list = []
    for race_number in race_numbers:
        person = generate_person_from_race_nubmer(race_location, race_number)
        people_list.append(person)

    people = People(people_list)

    return people


def ask_for_location() -> MightHikeLocation:
    """Ask user for location. If invalid keep asking until a valid location is
    given.

    Returns
    -------
    location: MightHikeLocation
        The location of the Mighty Hike as a member of the MightHikeLocation
        IntEnum.
    """
    invalid_location = True
    ask_string = "Enter the location id:\n"
    while invalid_location:
        user_input = input(ask_string)
        try:
            location_id = int(user_input)
            location = MightHikeLocation(location_id)
            invalid_location = False
            return location
        except:
            ask_string = (
                "Could not find that location id.\nPlease enter a valid lcoation id:\n"
            )
            pass
    raise RuntimeError


def ask_for_race_number() -> int:
    """Ask user for a race number. If invalid keep asking until a valid race
    number is given.

    Returns
    -------
    race_number: int
        The race number the user entered.
    """
    invalid_input = True
    ask_string = "Enter a race number:\n"
    while invalid_input:
        user_input = input(ask_string)
        try:
            race_number = int(user_input)
            assert race_number >= 0
            invalid_input = False
            return race_number
        except:
            ask_string = "Could not parse into an race_number.\nPlease enter a valid race number:\n"
            pass
    raise RuntimeError


def ask_for_race_numbers() -> list[int]:
    """Ask user for a series of race numbers. If any of the race numbers given
    are invalid it will keep asking until it gets atleast one valid race
    number. Will ask if the user wants to add more race numbers, if so will
    keep getting more valid race numbers until the user responds otherwise.

    Returns
    -------
    race_numbers: list[int]
        The list of race numbers the user entered.
    """
    race_numbers: list[int] = []
    add_more_numbers = True

    no_more_strings = ["", " ", "n", "N", "no", "No", "NO"]
    while add_more_numbers:
        race_number = ask_for_race_number()
        race_numbers.append(race_number)
        add_more_user_input = input("Add more race nubmer/numbers? `Y`/[`N`])\n")

        if add_more_user_input in no_more_strings:
            add_more_numbers = False
            break

    return race_numbers


def main():
    print("+---------------------+")
    print("|  Might Hike Plotter |")
    print("+---------------------+")
    print("")
    # while True:
    print("MightHikeLocations:\n")
    for member in MightHikeLocation:
        print(f"{member.value} : {member.name}")
    print("")
    location = ask_for_location()
    race_numbers = ask_for_race_numbers()

    people = generate_people_from_race_nubmers(location, race_numbers)
    people.plot()


def test():
    """."""
    location = MightHikeLocation.Jurassic_Coast
    race_numbers = [
        643,
        644,
        108,
        14,
        107,
        765,
    ]
    people = generate_people_from_race_nubmers(location, race_numbers)
    # people.plot()


if __name__ == "__main__":
    main()
