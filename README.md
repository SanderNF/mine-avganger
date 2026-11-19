[![Static Web Page](https://github.com/SanderNF/mine-avganger/actions/workflows/pages/pages-build-deployment/badge.svg)](https://sandernf.github.io/mine-avganger/)
# Mine avganger

A personal real-time departure dashboard for public transport in Norway. Put the trains, metro, trams, buses and boats you care about on one screen, filtered down to exactly the lines, directions and platforms you use.

It is a single HTML file with no build step, no server and no API key. Departure data comes from [Entur](https://developer.entur.no/), Norway's national journey planner, which covers every operator, including Vy, Ruter, SJ and Go-Ahead.

## Features

- Several departure boards on one page, each for any stop in Norway.
- Filters per board by transport type, line, platform, and destination for each line (for example RE10 towards Dombås but not towards Lillehammer).
- Travel chains: save a trip with several legs and changes, for example tram 12 or 15 from Glads vei to Jernbanetorget, a 5 minute walk, then RE10 from Oslo S to Lillestrøm. The board shows the next trips where every connection can be made, with real-time times for each leg. A travel board can hold alternative routes, for example metro 5 from Storo to Økern and a 7 minute walk, or bus 23/24 from Storo to Ulven torg and a 5 minute walk, sorted together by arrival or departure.
- Real-time times that count down in minutes close to departure, with delays, cancellations and disruption messages.
- Edit mode for adding, renaming, removing, resizing and reordering boards, by dragging or with arrow buttons.
- Light and dark themes that follow your system setting.
- Updates every 30 seconds.
- A header photo of the Oslo S clock tower (`IMGs/clock-tower.jpg`). If you host the page, upload the `IMGs` folder too.

## Getting started

Download `mine-avganger.html` and open it in a web browser. It needs an internet connection to reach Entur.

The page will not load departures inside a sandboxed preview (such as the file preview in Claude), because those block requests to other websites. Open it in a normal browser tab instead.

## Using the dashboard

1. Click **Rediger** to enter edit mode.
2. Click **Legg til tavle** to add a board, search for a stop and choose it.
3. Tap the transport types, lines and platforms you want to see. Leaving a group empty shows everything.
4. For each selected line, use the **Retning per linje** dropdown to pick one destination, or leave it on **Alle retninger**.
5. Optionally give the board a name, the number of departures to show and a width.
6. Drag boards, or use **←** and **→**, to change the order. Click the page title to rename the dashboard.
7. Click **Ferdig** when you are done.

### Travel chains

1. In edit mode, click **Legg til reise**.
2. For each leg, choose where you get on (**Fra**) and where you get off (**Til**). The line chips then show every line that runs directly between the two, including lines that only run at other times of day. Pick the ones you use, or leave them all off to allow any of them. Stops within 250 metres count as the same place, so **Oslo S** also covers the trams and buses at Jernbanetorget, and each leg on the board shows the stop actually used.
3. Set the walking time: for the first leg, the time it takes to walk to the first stop; for later legs, the time you need to walk and change from the previous one.
4. Click **+ Legg til etappe** for each change.
5. Optionally set the walk from the last stop to where you are going. Routes that end at different stops are then compared by when you actually get there.
6. To add another way to make the same trip, click **+ Legg til alternativ rute** and set it up the same way. With more than one route, **Sorter reisene etter** decides the order: **Ankomst** (the default) puts the trip that gets you there first at the top, **Avgang** the one that leaves first.
7. Click **Legg til reise**.

Each row on the board is one trip: when to leave, when you arrive, and every leg with times, track and any waiting time. When several early departures lead to the same final connection, only the latest one is shown, so you never leave earlier than you need to. If one of several routes has no trips, for example while a metro line is replaced by buses, the note under the board says so.

Your setup is saved in the browser's local storage. It stays when you close the page, but it does not follow you to another browser or device.

## Hosting on GitHub Pages

1. Create a repository and add `mine-avganger.html`. Rename it to `index.html` if you want the dashboard at the repository's root address.
2. In the repository, go to **Settings → Pages**, choose **Deploy from a branch**, select your main branch and the root folder, and save.
3. After a minute or so the dashboard is live at `https://<username>.github.io/<repository>/`.

The **GitHub** button in the header links to [sandernf/mine-avganger](https://github.com/sandernf/mine-avganger), set with `REPO_URL` (see below). If you fork the project, change it to your own repository, or set it to an empty string and the button will find the repository automatically on GitHub Pages.

## Configuration

These constants are at the top of the script in the HTML file:

| Constant | What it does |
| --- | --- |
| `CLIENT_NAME` | Identifies your app to Entur. Entur asks for the form `company-application`, for example `yourname-mineavganger`. |
| `REPO_URL` | Link for the GitHub button. Set to `https://github.com/sandernf/mine-avganger`; empty means automatic detection on GitHub Pages. |
| `REFRESH_MS` | How often departures are fetched, in milliseconds. Default `30000`. |

## Data source

- Departures: [Entur Journey Planner v3](https://developer.entur.no/docs/open-services/journey-planner) (GraphQL).
- Stop search: Entur Geocoder.

Entur's data is open and licensed under the Norwegian Licence for Open Government Data (NLOD). Requests must include the `ET-Client-Name` header, which the page sends using `CLIENT_NAME`.

## Known limitations

- Large hubs are separate stops in Entur, and departure boards (unlike travel chains) show one stop each. For example, Oslo S has the trains and Jernbanetorget has the metro, trams and buses, so add a board for each.
- The destination filter matches the destination shown on the departure, which is where the trip ends. A train to Dombås does not count as "Lillehammer" even though it stops there.
- Travel chains only use direct trips within each leg, and use the walking times you set rather than Entur's own change times. Connections are worked out from departures on the chosen lines in the next 12 hours, up to 200 per stop.
- The 250 metre rule is measured from the stop you choose, so it is not always symmetric: Oslo S includes Jernbanetorget (236 m), but Jernbanetorget does not include Oslo S, since the stations' centre points are 343 m apart.
- Each board shows departures from the next 12 hours, up to 200 per stop before filtering, so very selective filters at busy stops may show few results.
- Stop search uses Entur's Geocoder v1, which Entur deprecated on 12 June 2026 in favour of Geocoder v3. If stop search stops working, it needs to be moved to v3.

## License

No license has been chosen yet. Add one if you want others to reuse the code.
