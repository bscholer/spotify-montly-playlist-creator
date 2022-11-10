# ⚙ Config File ⚙

For example, see `example/config.json`.

## Fields

* `version`: The version of the config file. This is used to determine if the config file is compatible with the current version of the program.
* `period_playlist`: Array of period playlist configurations
    * `enabled`: Will period playlists be created based on this configuration?

      `true` or `false`
    * `period`: How often new playlists will be created

      `string`, either `daily`, `weekly`, `monthly`, or `yearly`
  
      example: `monthly`
    * `only_process_current_period`: If enabled, only create and add songs to the playlist for the current `period`

      `true` or `false`
    * `playlist_name`: The name of the playlist to create

      `string`, which can have [`{date injections}`](#date-injections) and an [`|alliteration|`](#alliterations)

      example: "`{now>YY}` `|{now>MMMM}|` `{now>MMMM}`" yields "22 Anxious April"
    * `playlist_description`: The description of the playlist to create

      `string`, which **must** have `$date_key`, and, if `playlist_name` has an [`|alliteration|`](#alliterations), **must** have `$alliteration_key`

      example: "🤖 generated `$alliteration_key` playlist for `$date_key`" yields "🤖 generated ✨Anxious✨ playlist for 📆2022-04📆"
    * `date_key`: Used to match playlists so that duplicates aren't created

      `string` with a prefix, and a [`{date injection}`](#date-injections), appropriate for the `period`.

      example: `📆{now>YYYY-MM}📆`
    * `alliteration_key_wrapper`: What to wrap the alliteration word with in the description. Used to screen out already-used
      alliterations from the word list.

      `string`

      example: `✨`
    * `public`: Is the playlist public?

      `true` or `false`
    * `collaborative`: Is the playlist collaborative?

      `true` or `false`
    * `minimum_tracks`: The inclusive minimum number of tracks to add to the playlist

      `integer`
  
      example: `2`
    * `alliteration_word_list`: A list of words to use for alliterations

      `[strings]`

      (way too short) example: `["anxious", "accidental", "absent", "delicate", "fancy", "macho"]`
  
* `backups`: Array of backup configurations
    * `enabled`: Will backups be created based on this configuration?

      `true` or `false`
    * `original_id`: The ID of the playlist to back up
    * `original_name`: The name of the playlist to back up. Used if `original_id` is not found.
    * `backup_name`: The name of the backup playlist to create
    * `backup_description`: The description of the backup playlist to create
    * `date_key`: Used to match playlists so that duplicates aren't created
    * `public`: Is the playlist public?
    * 
      "backup_name": "DW {last monday>YYYY-MM-DD}",
      "backup_description": "🤖 generated backup playlist for Discover Weekly {date_key}",
      "date_key": "🔎{last monday>YYYY-MM-DD}",
      "backup_public": false,
      "backup_collaborative": false,
      "use_cover_art_from_original": false,
      "cron_statement": "0 0 * * WED"

## Date Injections

**TL;DR**: `{start of week>YYYY-MM-DD}` will yield `2022-04-18`

Date injections are used to inject dates into the playlist name and description.

They consist of two parts, the date and the formatter, separated with `>`, and surrounded by `{}`. The date is parsed to
obtain the date to inject, and the formatter is used to format the date.

* Dates are parsed using the [chrono](https://github.com/wanasit/chrono) library, and supports relative dates, such
  as *"today"*, *"yesterday"*, *"tomorrow"*, *"next week"*, *"last month"*, etc.

  These will be calculated anytime the program runs. So, for example, monthly playlists need injections of something
  like `{now>MMMM}` to get the current month.

* Formatters use the [dayjs](https://day.js.org/docs/en/display/format) library. Common formatters are `YYYY` -> **2022**, `MM` -> **04**, `DD` -> **20**, etc.

### Examples Table 

*Examples based on today being 2022-04-20*

| Date Injection                  | Result         |
|---------------------------------|----------------|
| `{this past Monday>YYYY-MM-DD}` | **2022-04-18** |
| `{today>YYYY-MM-DD}`            | **2022-04-20** |
| `{now>YYYY-MM}`                 | **2022-04**    |
| `{start of month>YYYY-MM}`      | **2022-04**    |
| `{now>MMMM}`                    | **April**      |
| `{today>MMMM YYYY}`             | **April 2022** |

## Alliterations

**TL;DR**: `|{now>MMMM}|` could yield `Absent`

Alliterations are used to inject alliterations into the playlist name. They are surrounded by `||`, and can have a date
injection inside them.

Whatever is inside the alliteration will be used to find a word in the alliteration word list that starts with the same
letter.

If the word list is empty (or all are already being used in a playlist), the alliteration will be replaced with an empty
string.

### Examples Table

Using word list: `["anxious", "accidental", "absent", "delicate", "fancy", "macho"]`

| Alliteration             | 'Current' Date | Resolves to | Result      |
|--------------------------|----------------|-------------|-------------|
| `&#124;{now>MMMM}&#124;` | 2022-04-20     | April       | **Anxious** |
| `&#124;{now>DDDD}&#124;` | 2022-04-18     | Monday      | **Macho**   |
| `&#124;{now>DDDD}&#124;` | 2022-02-01     | February    | **Fancy**   |


### Config File Versions

| Project Version | Config File Version |
|-----------------|---------------------|
| 1.0.0           | 1                   |


