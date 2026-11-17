[![Static Web Page](https://github.com/SanderNF/mine-avganger/actions/workflows/pages/pages-build-deployment/badge.svg)](https://sandernf.github.io/mine-avganger/)
# Mine avganger

A personal real-time departure dashboard for public transport in Norway. Put the trains, metro, trams, buses and boats you care about on one screen, filtered down to exactly the lines, directions and platforms you use.

It is a single HTML file with no build step, no server and no API key. Departure data comes from [Entur](https://developer.entur.no/), Norway's national journey planner, which covers every operator, including Vy, Ruter, SJ and Go-Ahead.

## Features

- Several departure boards on one page, each for any stop in Norway.
- Filters per board by transport type, line, platform, and destination for each line (for example RE10 towards Dombås but not towards Lillehammer).
- Real-time times that count down in minutes close to departure, with delays, cancellations and disruption messages.
- Edit mode for adding, renaming, removing, resizing and reordering boards, by dragging or with arrow buttons.
- Light and dark themes that follow your system setting.
- Updates every 30 seconds.

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

- Large hubs are separate stops in Entur. For example, Oslo S has the trains and Jernbanetorget has the metro, trams and buses, so add a board for each.
- The destination filter matches the destination shown on the departure, which is where the trip ends. A train to Dombås does not count as "Lillehammer" even though it stops there.
- Each board shows departures from the next 12 hours, up to 200 per stop before filtering, so very selective filters at busy stops may show few results.
- Stop search uses Entur's Geocoder v1, which Entur deprecated on 12 June 2026 in favour of Geocoder v3. If stop search stops working, it needs to be moved to v3.

## License

No license has been chosen yet. Add one if you want others to reuse the code.
