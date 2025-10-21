//GNU nano 7.2                                                                                                                                                                                                                          config.js *
/* Config Sample
 *
 * For more information on how you can configure this file
 * see https://docs.magicmirror.builders/configuration/introduction.html
 * and https://docs.magicmirror.builders/modules/configuration.html
 *
 * You can use environment variables using a `config.js.template` file instead of `config.js`
 * which will be converted to `config.js` while starting. For more information
 * see https://docs.magicmirror.builders/configuration/introduction.html#enviromnent-variables
 */
let config = {
        address: "localhost",   // Address to listen on, can be:
                                                        // - "localhost", "127.0.0.1", "::1" to listen on loopback interface
                                                        // - another specific IPv4/6 to listen on a specific interface
                                                        // - "0.0.0.0", "::" to listen on any interface
                                                        // Default, when address config is left out or empty, is "localhost"
        port: 8080,
        basePath: "/",  // The URL path where MagicMirror² is hosted. If you are using a Reverse proxy
                                                                        // you must set the sub path here. basePath must end with a /
        ipWhitelist: ["127.0.0.1", "::ffff:127.0.0.1", "::1"],  // Set [] to allow all IP addresses
                                                                                // or add a specific IPv4 of 192.168.1.5 :
                                                                        // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.1.5"],
                                                                        // or IPv4 range of 192.168.3.0 --> 192.168.3.15 use CIDR format :
                                                                        // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.3.0/28"],

        useHttps: false,                        // Support HTTPS or not, default "false" will use HTTP
        httpsPrivateKey: "",    // HTTPS private key path, only require when useHttps is true
        httpsCertificate: "",   // HTTPS Certificate path, only require when useHttps is true

        language: "en",
        locale: "en-US",
        logLevel: ["INFO", "LOG", "WARN", "ERROR"], // Add "DEBUG" for even more logging
        timeFormat: 24,
        units: "metric",

        modules: [
                {
                        module: "alert",
                },
                {
                        module: "clock",
                        position: "top_left"
                },
                {
                        module: "calendar",
                        header: " ",
                        position: "top_left",
                        config: {
                                calendars: [
                                        {
                                                fetchInterval: 10 * 60 * 1000,
                                                symbol: "calendar-check",
                                                url: "https://outlook.office365.com/owa/calendar/b576cd8094e14422b2c5f16c35737dac@vt.edu/f0b365ebffec4e63a29029708a2024dd4484729958005958732/calendar.ics",
                                                maximumNumberofDays: 1

                                        }
                                ]
                        }
                },
                {
                        module: "compliments",
                        position: "lower_third", // This can be any of the regions.
                        // Best results in one of the middle regions like: lower_third
                        config: {
                                updateInterval: 300000,
                                classes: "compliments",
                                compliments: {
                                        anytime: [
                                                "“Freedom consists not in doing what we like, but in having the right to do what we ought.” - Pope John Paul II",
                                                "“Do not be afraid. Do not be satisfied with mediocrity. Put out into the deep and let down your nets for a catch.” - Pope John Paul II",
                                                "“Joy, with peace, is the sister of charity. Serve the Lord with laughter.“ - Padre Pio",
                                                "“Pray, hope, and don’t worry.“ - Padre Pio",
                                                "”Be who you are and be that well.” - St Francis De Sales",
                                                "”You learn to speak by speaking, to study by studying, to run by running, to work by working; and just so, you learn to love by loving.” - St Francis De Sales",
                                                "”Do not become upset when difficulty comes your way. Laugh in its face and know that you are in the hands of God.” - St Francis De Sales",
                                                "”Jesus is with me. I have nothing to fear.” - Blessed Pier Giorgio Frassati",
                                                "”When God is with us, we don’t have to be afraid of anything.” - Blessed Pier Giorgio Frassati",
                                                "”The world offers you comfort. But you were not made for comfort. You were made for greatness” - Pope Benedict XVI",
                                                "”Do not put off till tomorrow the good you can do today. You may not have a tomorrow.” - St. John Boscoe",
                                                "”If you judge people, you have no time to love them.” - Mother Teresa",
                                        ],
                                },
                        },
                },
                {
                        module: "weather",
                        position: "top_right",
                        config: {
                                weatherProvider: "openweathermap",
                                type: "current",
                                location: "Blacksburg",
                                locationID: "4747845", //ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and find your city
                                tempUnits: "imperial",
                                windUnits: "imperial",
                                apiKey: "f2dc7f05ff69c9e8c65c43bad39d3a83"
                        }
                },
                {
                        module: "weather",
                        position: "top_right",
                        header: "Weather Forecast",
                        config: {
                                weatherProvider: "openweathermap",
                                type: "forecast",
                                location: "Blacksburg",
                                locationID: "4747845", //ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and find your city
                                tempUnits: "imperial",
                                windUnits: "imperial",
                                apiKey: "f2dc7f05ff69c9e8c65c43bad39d3a83"
                        }
                },
                {
                        module: 'MMM-BackgroundSlideshow',
                        position: 'fullscreen_below',
                        config: {
                                imagePaths: ['modules/MMM-BackgroundSlideshow/images/'],
                                transitionImages: false,
                                slideshowSpeed: 2147483600,
                                }
                },
                {
                        module: "newsfeed",
                        position: "bottom_bar",
                        config: {
                                feeds: [
                                        {
                                                title: "USCCB Daily Readings",
                                                url: "https://bible.usccb.org/readings.rss",
                                        },
                                        {
                                                title: "Saint of the Day",
                                                url: "https://feeds.feedburner.com/catholicnewsagency/saintoftheday"
                                        },
                                ],
                                showSourceTitle: true,
                                showPublishDate: true,
                                broadcastNewsFeeds: true,
                                broadcastNewsUpdates: true,
                                showDescription: true,
                                updateInterval: 200000,
                        }
                },
        ]
};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") { module.exports = config; }