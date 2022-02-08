# Implementation
Execute the following sequence of commands in the terminal to conduct the data parsing procedure: 

1) Download and extract HTML files from Google Drive
```shell
bash 00_loadData.sh
```
2) Parse data
```shell
python 01_parseData.py
```
3) Load data to MongoDB
```shell
python 02_jsonToMongo.py
```

# MetaData
 - For sample records, please see [./sampleRecords](https://github.com/simoneSantoni/music-market/tree/master/rateYourMusic/parseData/sampleRecords).
 - Example for each field does not necessary come from the same html (For illustration purpose).
 - If the `Request Type (K8)` is `"New"`, `K9` onward only consider `Current Profile (V0)` – All `New Profile (V1)` is `NULL` <sup id="note1">[*](#note1)</sup>


|        Keys        |        Variables        |    <div align='middle'>Description</div>    |<div align='middle'>Example</div>|                 
|:------------------:|:-----------------------:|:--------------------------------------------|:--------------------------------|
|     thread_id      |           -             | Thread ids                                  | "29"                            |
|         K1         |           V0            | Whether the genre profile is `New` or `Edit`| "Music genre Profile (New)"     |
|         K2         |           V0            | Genre Name                                  | "West Coast Hip Hop"            |
|                    |           V1            | Genre Name (with Hyperlink)                 | ["West Coast Hip Hop", "/genre/west-coast-hip-hop/"] |
|                    |           V2            | Genre Id                                    | "[genre29]"                     |
|         K3         |           V0            | Submitted by (with Hyperlink)               | ["\_aleph"", "/~\_aleph"]       |
|         K4         |           V0            | Submit Time                                 | "2008-03-27 10:25:13.49987"     |
|         K5         |           V0            | Approval Status                             | "Approved by sharifi on 2019-11-04 10:33:51.341954" |
|                    |           V1            | User who granted approval (with Hyperlink)  | ["sharifi", "/~sharifi"]        |
|         K6         |           V0            | Number of comments                          | "131"                           |
|         K7         |           V0            | Percentage of `Yes` votes over total votes  | "85%"                           |
|                    |           V1            | Number of `Yes` votes                       | "Yes: 107"                      |
|                    |           V2            | Number of `Hold` votes                      | "Hold:3"                        |
|                    |           V3            | Number of `No` votes                        | "No: 15"                        |
|         K8         |           V0            | Request Type                                | "New"                           |
|         K9         |           V0            | Contributor (Old \| Current Profile)<sup>[*](#note1)</sup>             | ["\_aleph"", "/~\_aleph"] |
|                    |           V1            | Contributor (New Profile)<sup>[*](#note1)</sup>                        | ["Ensix", "/~Ensix"]      |
|         K10        |           V0            | First Name (Old \| Current Profile)<sup>[*](#note1)</sup>              | ""                        |
|                    |           V1            | First Name (New Profile)<sup>[*](#note1)</sup>                         | ""                        |
|         K11        |           V0            | Last Name (Old \| Current Profile)<sup>[*](#note1)</sup>               | "Melodic Dubstep"         |
|                    |           V1            | Last Name (New Profile)<sup>[*](#note1)</sup>                          | "Melodic Dubstep"         |
|         K12        |           V0            | Genre ID (Old \| Current Profile)<sup>[*](#note1)</sup>                | "10321"                   |
|                    |           V1            | Genre ID (New Profile)<sup>[*](#note1)</sup>                           | "10321"                   |
|         K13        |           V0            | AKAs (Old \| Current Profile)<sup>[*](#note1)</sup>                    | "Liquid Dubstep, Lovestep"|
|                    |           V1            | AKAs (New Profile)<sup>[*](#note1)</sup>                               | "Liquid Dubstep, Lovestep"|
|         K14        |           V0            | Parent genre (Old \| Current Profile)<sup>[*](#note1)</sup>            | "show tunes, opera (455) (190)"|
|                    |           V1            | Parent genre (New Profile)<sup>[*](#note1)</sup>                       | "opera (190)"|
|         K15        |           V0            | Can be rated on a scale (Old \| Current Profile)<sup>[*](#note1)</sup> | "No"|
|                    |           V1            | Can be rated on a scale (New Profile)<sup>[*](#note1)</sup>            | "No"|
|         K16        |           V0            | Top level (Old \| Current Profile)<sup>[*](#note1)</sup>               | "No"|
|                    |           V1            | Top level (New Profile)<sup>[*](#note1)</sup>                          | "No"|
|         K17        |           V0            | Is category only (Old \| Current Profile)<sup>[*](#note1)</sup>        | "No"|
|                    |           V1            | Is category only (New Profile)<sup>[*](#note1)</sup>                   | "No"|
|         K18        |           V0            | Type (Old \| Current Profile)<sup>[*](#note1)</sup>                    | "genre"|
|                    |           V1            | Type (New Profile)<sup>[*](#note1)</sup>                               | "genre"|
|         K19        |           V0            | Description Short (Old \| Current Profile)<sup>[*](#note1)</sup>       | "Stripped-down and sparse, often featuring a dark sound and a slow, steady development through the track."|
|                    |           V1            | Description Short (New Profile)<sup>[*](#note1)</sup>                  | "Stripped-down and sparse, often featuring a dark sound and a slow, steady development through the track."|
|         K20        |           V0            | Description (Old \| Current Profile)<sup>[*](#note1)</sup>             | "Minimal Techno is a stripped-down, sparser version of traditional Techno, often featuring a darker sound and a slow, steady development ..."|
|                    |           V1            | Description (New Profile)<sup>[*](#note1)</sup>                        | "Developing in the early 1990s out of the second wave of Detroit Techno by artists in Detroit and Southern Ontario such as ..."|
|         K21        |           V0            | Meta Comments (Old \| Current Profile)<sup>[*](#note1)</sup>           | "http://en.wikipedia.org/wiki/Minimal_techno"|
|                    |           V1            | Meta Comments (New Profile)<sup>[*](#note1)</sup>                      | "http://en.wikipedia.org/wiki/Minimal_techno---New description. Sources:https://en.wikipedia.org/wiki/ ..."|
|         K22        |           V0            | Hyperlink in Description (K20) (Old \| Current Profile)<sup>[*](#note1)</sup>   | \*JSON Format with keys: `"class"`, `"href"`, `"title"`, `"text"`|
|                    |           V1            | Hyperlink in Description (K20) (New Profile)<sup>[*](#note1)</sup>              | \*JSON Format with keys: `"class"`, `"href"`, `"title"`, `"text"`|
|         K23        |           V0            | Hyperlink in Meta Comments (K21) (Old \| Current Profile)<sup>[*](#note1)</sup> | \*JSON Format with keys: `"class"`, `"href"`, `"title"`, `"text"`|
|                    |           V1            | Hyperlink in Meta Comments (K21) (New Profile)<sup>[*](#note1)</sup>            | \*JSON Format with keys: `"class"`, `"href"`, `"title"`, `"text"`|
|         K24        |            -            | Comments                    | \*JSON Format with keys: <ul><li>`"V0"`: Username</li><li>`"V1"`: User's href</li><li>`"V2"`: Comment</li><li>`"V3"`: Comment's href (`Type: List`)</li><li>`"V4"`: Vote ("y", "n")</li><li>`"V5"`: Timestamp</li>|

 Note: For href in the comment (`K24`), if an element in the list contains the string: `'javascript:toggleChange'`, the comment was there because there was an update to the profile request.
 
 # Sample Annotation
 For full-size images, please see [./sampleAnnotations](https://github.com/simoneSantoni/music-market/tree/master/rateYourMusic/parseData/sampleAnnotations).
 - Edit (Request Type)
<p align="center" width="100%">
     <img width="49%" height="49%" src="https://github.com/simoneSantoni/music-market/blob/master/rateYourMusic/parseData/sampleAnnotations/edit-1.jpg">
     <img  width="49%" height="49%" src="https://github.com/simoneSantoni/music-market/blob/master/rateYourMusic/parseData/sampleAnnotations/edit-2.jpg">
</p>
 
 - New (Request Type)
 <p align="center" width="100%">
      <img width="49%" height="49%" src="https://github.com/simoneSantoni/music-market/blob/master/rateYourMusic/parseData/sampleAnnotations/new-1.jpg">
      <img width="49%" height="49%" src="https://github.com/simoneSantoni/music-market/blob/master/rateYourMusic/parseData/sampleAnnotations/new-2.jpg">
 </p>
