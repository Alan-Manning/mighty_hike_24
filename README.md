# Mighty Hike Plotter

Create a plot of times for the mighty hike from race numbers.

See usage below.

## Example plot
![alt text](https://github.com/Alan-Manning/mighty_hike_24/blob/main/MightHike_2024_plot.png?raw=true)

## Usage
Clone the repo.
```console
foo@bar:~$ git clone https://github.com/Alan-Manning/mighty_hike_24.git
```
or you can download the zip file from the top left of this page.

Change directory into the new folder.
```console
foo@bar:~$ cd mighty_hike_24
```

Install the requirements.
```console
foo@bar:~$ pip install requirements.txt
```

Run the program.
```console
foo@bar:~$ python main.py
```

This will run the main.py python file which will ask you for your location id
out of the possible locations.

```console
+---------------------+
|  Might Hike Plotter |
+---------------------+

MightHikeLocations:

20439 : Wye_Valley
20440 : Jurassic_Coast
20437 : Rob_Roy
20438 : Cornwall_Coast
20436 : Peak_District
20435 : Thames_Path
20434 : Gower_Peninsula
20433 : Yorkshire_Dales
20432 : Giants_Causeway
20431 : Lake_District
20430 : South_Coast
20429 : London
20428 : Eryri_Snowdonia
20427 : Norfolk_Coast

Enter the location id:
```

Enter in your location id. e.g. mine was `20440` which was the `Jurassic_Coast`
Mighty Hike.

It will then ask you to enter a race number.

```console
Enter a race number:
643
```
Enter in your race number. e.g. mine was `643`.

```console
Add more race nubmer/numbers? `Y`/[`N`])
```
If you only want to plot your numbers type `N` or nothing. If you want to add
your friends race numbers so you can compare your times vs thiers you can type
`Y`. If you do add more then the same promt will appear again. Keep adding
more race numbers untill your done.

Once your have entered `N` the script will try grabbing all the leg times and
total time from the online results page.
[Mighty Hikes Results](https://results.resultsbase.net/StartPage.aspx?CId=8&c=21&S=2024)

If everything has gone to plan then you should see the script start converting the race numbers into data.

```console
Succesfully parsed data for race number `643` -> Alan Manning.
Succesfully parsed data for race number `644` -> Sabrina Manning.
Succesfully parsed data for race number `108` -> Natalie Boulton.
Succesfully parsed data for race number `14` -> Ollie Anderson.
Succesfully parsed data for race number `107` -> George Boulton.
Succesfully parsed data for race number `765` -> Gemma Orman.
Saved plot as MightHike_2024_plot.png
```
The plot gets saved as `MightHike_2024_plot.png` which is what you can see at
the top of this page.



# Issues

## Known Issues

Please note that in my very brief look at the other Mighty Hikes it appears
that not all the leg times are recorded and some have no leg times and just
split times. This will throw an error and will be unable to take the race
number / numbers and plot them automatically.

Essentially. If your output from the [Mighty Hikes Results](https://results.resultsbase.net/StartPage.aspx?CId=8&c=21&S=2024) page does not look like this below, then you might be
out of luck.

![alt text](https://github.com/Alan-Manning/mighty_hike_24/blob/main/Desired_results_page.png?raw=true)


If you feel you would like to try to fix this please feel free to submit a
pull request for me to review.

### Manually add data
If you cant get the results to automatically load in then you can edit the
main.py file to add your data manually.

To do this open the main.py file in any text editor you like. Get rid of the
code in the `main()` function at the bottom of the file.
```python
def main():
    # print("+---------------------+")
    # print("|  Might Hike Plotter |")
    # print("+---------------------+")
    # print("")
    # # while True:
    # print("MightHikeLocations:\n")
    # for member in MightHikeLocation:
    #     print(f"{member.value} : {member.name}")
    # print("")
    # location = ask_for_location()
    # race_numbers = ask_for_race_numbers()
    #
    # people = generate_people_from_race_nubmers(location, race_numbers)
    # people.plot()
```

Now make your own dictionary with data. The keys are strict so should remain
the same, but the values (e.g.`"Alan"` for the `name` key) can be changed to
your own data you define. The `start`, `pitstop_1`... should all be time stamps
in the format `HH:MM:SS` (`HH` 24 hour format, `MM` is minutes, and `SS` is
seconds).

```python
def main():
    alan_times: dict[str, Any] = {
        "name": "Alan Manning",
        "race_number": 643,
        "start": "07:31:21",
        "pitstop_1": "09:42:58",
        "pitstop_2": "12:31:01",
        "pitstop_3": "14:23:02",
        "finish": "17:14:53",
    }
    sabrina_times: dict[str, Any] = {
        "name": "Sabrina Manning",
        "race_number": 644,
        "start": "07:31:19",
        "pitstop_1": "09:44:47",
        "pitstop_2": "12:35:30",
        "pitstop_3": "14:22:59",
        "finish": "17:36:35",
    }
    ...
```

You then need to construct a `Person` object for each person and then a
`People` object with the people. Then you can call the `plot()` method on the
people object and it should work.

```python
def main():
    alan_times: dict[str, Any] = {
        "name": "Alan Manning",
        "race_number": 643,
        "start": "07:31:21",
        "pitstop_1": "09:42:58",
        "pitstop_2": "12:31:01",
        "pitstop_3": "14:23:02",
        "finish": "17:14:53",
    }
    sabrina_times: dict[str, Any] = {
        "name": "Sabrina Manning",
        "race_number": 644,
        "start": "07:31:19",
        "pitstop_1": "09:44:47",
        "pitstop_2": "12:35:30",
        "pitstop_3": "14:22:59",
        "finish": "17:36:35",
    }

    Alan = Person(**alan_times)
    Sabrina = Person(**sabrina_times)

    list_of_people = [ Alan, Sabrina]

    people = People(list_of_people)
    people.plot()
```

now when you run the script using:
```console
foo@bar:~$ python main.py
```
You should get your plot generated and saved.


## Other Issues And Feature Requests
If you still have issues and you think everything is right, or to request a
new feature or extend existing features please create a github issue at the
top of this page.



