# ⚙ Config File ⚙

For example, see `example/config.json`.

## Fields
* `period_playlist`: array of period playlist configurations
    * `enabled`: Will period playlists be created based on this configuration?

      `true` or `false`
    * `period`: How often new playlists will be created
  
      `string`, either `daily`, `weekly`, `monthly`, or `yearly`
    * `only_process_current_period`: If enabled, only create and add songs to the playlist for the current period
  
      `true` or `false`
    * `playlist_name`: The name of the playlist to create
  
      `string`, which can have [`{date injections`](#date-injections) and an [`|alliteration|`](#alliteration)
      
      example: `{now>YY} |{now>MMMM}| {now>MMMM}`
    * `playlist_description`: The description of the playlist to create
  
      `string`, which **must** have `{date_key}`, and, if `playlist_name` has an alliteration, `{alliteration_key}`
  
      example: `🤖 generated {alliteration_key} playlist for {date_key}`
    * `date_key`: Used to match playlists so that duplicates aren't created
  
      `string` with a prefix, and a date injection matching the period.
  
      example: `📆{now>YYYY-MM}`
    * `alliteration_key_prefix`: The prefix for the alliteration key. Used to identify and remove already-used alliterations from the word list.
  
      `string`
  
      example: `✨`,
    * `public`: Is the playlist public?
  
      `true` or `false`
    * `collaborative`: Is the playlist collaborative?
  
      `true` or `false`
    * `minimum_tracks`: The minimum number of tracks to add to the playlist
  
      `integer`
    * `alliteration_word_list`: A list of words to use for alliterations
  
      `array of strings`
       
      example: `["long", "list", "of", "words"]`

## Date Injections

TL;DR: `{start of week>YYYY-MM-DD}` will yield `2022-04-18`

Date injections are used to inject dates into the playlist name and description. 

They consist of two parts, the date and the formatter, separated with `>`, and surrounded by `{}`. The date is parsed to obtain the date to inject, and the formatter is used to format the date.

* Dates are parsed using the [chrono](https://github.com/wanasit/chrono) library, and supports relative dates, such as `today`, `yesterday`, `tomorrow`, `next week`, `last month`, etc.

    These will be calculated anytime the program runs. So, for example, monthly playlists need an injection of something like `{now>MMMM}` to get the current month.

* Formatters use the [dayjs](https://day.js.org/docs/en/display/format) library. Common formatters are `YYYY` -> `2022`, `MM` -> `04`, `DD` -> `20`, etc.

### Examples (based on today being 2022-04-20)

* `{this past Monday>YYYY-MM-DD}`: `2022-04-18`
* `{today>YYYY-MM-DD}`: `2022-04-20`
* `{now>YYYY-MM}`: `2022-04`
* `{start of month>YYYY-MM}`: `2022-04`
* `{now>MMMM}`: `April`
* `{today>MMMM YYYY}`: `April 2022`