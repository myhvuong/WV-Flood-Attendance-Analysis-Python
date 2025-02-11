### Research Question
 In this project, I will discuss and answer the question of whether or not flooding has an impact on school attendance using data and evidence from West Virginia, one of the nation's most flood-prone states, from 2003 to 2023. The underlying motivation for this study lies in conducting a non-market valuation, recognizing that the impact of natural disasters extends beyond conventional market values. Also, much of the past literature has discussed the effects of natural disaster events on student learning and achievement. However, none has covered the specific impacts of flooding on school attendance. Given the direct correlation between school absences and education outcomes, this research contributes to the literature by providing more insights into the ways through which natural disasters, specifically flooding, affect student performance in the context of West Virginia's unique challenges. 
 
### Data Wrangling
*Attendance* – The education outcome parameter in this analysis is measured in attendance rate per school year. The data is obtained from the West Virginia Department of Education’s Zoom WV and is aggregated on the county and school-year level. 
  
*Precipitation* – An important bulk of the project requires processing precipitation data retrieved from the National Centers for Environmental Information's (NCEI) Global Historical Climatology Network. The dataset provides precipitation information, measured in millimeters, from different weather stations on a county level. I extracted daily data records from stations that fall within the 2003-2023 period and found each station's total precipitation level in a given school year. The processed station data for all counties is then combined into a single data frame, which is used to aggregate the average precipitation level per school year for each county. Because heavy rain and storms usually occur during the summer months, when schools are closed, including rainfall data within this time frame would lead to an overestimation of the effect. Therefore, to have a cleaner capture of the impact of flooding on attendance rate, for each station, I eliminated any data points that fell outside of the school year to include only weather entries within the timeframe from September to May. Because not all schools start earlier in August and end later in June, I choose not to include these months for a more conservative approach. 
  
*Flood Incidents* — Recognizing that precipitation alone does not necessarily signify flooding, I retrieved historical disaster declaration data in West Virginia from 2003-2023, declared by the Federal Emergency Management Agency (FEMA) using APIs to measure the specific effects of floods on attendance. To quantify the number of flood incidents per school year for each county, I identified incident declarations containing the term 'FLOODING' in their titles. Similar to processing precipitation data, I consider only incidents that begin and end within the months that schools are in session. 

### Plotting

  1. Interactive Plots:
  
*Risk Map* – An interactive map of the four selected counties in West Virginia (Cabell, Grant, Kanawha, and Nicholas) colored by the level of flood risk. The location of a selected county will be highlighted on the map.
Flood Incident Plot – A bar plot showing the total number of flood incidents for the four counties, selected by school-year.

  2. Static Plots:
  
*Attendance Rate Trend* – Illustrates a trend in attendance rate with four subplots representing each county. The x-axis denotes the school year, while the y-axis reflects the attendance rate.

*Precipitation Level Trend* – Depicts a similar plot illustrating the trend in average precipitation levels, measured in millimeters, with precipitation on the y-axis. 
  
### Text Processing

I retrieve information on the risk level associated with each county from the Risk Factor webpages. The HTML content is parsed using BeautifulSoup and then converted into a large string for text processing. I took this text processing approach instead of web scraping using specific tags, given the web pages' large and complex nested structure. The desired information is bolded, making it more convenient to employ regular expressions for locating within a string. The extracted information is subsequently written into a CSV file, and this file is utilized in creating the risk map mentioned above. 

### Analysis and Results
I ran multiple regression models using Precipitation and Flood Counts as explanatory variables to estimate the effects of flooding on school attendance. Among the various models, the full OLS regression with Precipitation, Flood Incidents, and an interaction term between the two variables, along with a county fixed effects on the right-hand side, yields the highest R-squared value and can best explain the relationship between flooding and school attendance. 

The sign of the coefficient on the Flood Count variable is negative, which aligns with the expectation of a negative causal relationship between the number of flood counts and attendance rate. Specifically, as the count of flood incidents increases by one unit within a school year, the model predicts a 3.5 percentage point decrease in the attendance rate. Although the results are not statistically significant, the p-value associated with Flood Counts of 0.068 is close to being significant at the 5% significance level. With a larger dataset covering multiple counties, we might be able to get a statistically significant result on the Flood Count variable. Precipitation is similarly negative and statistically insignificant, though it has a small coefficient close to 0, indicating economic insignificance. This result intuitively makes sense, as the rainfall level alone may not necessarily imply actual flooding. A county might experience a high cumulative rainfall in a school year, but the rain intensity each time may not be severe enough to impact school absences significantly. 

### Future Research and Weaknesses
  1. Future Research

The findings in this research can inform valuable education policy recommendations. Recognizing how flooding may hinder student attendance, educators and school administrators can enhance accessibility by facilitating remote attendance options. Utilizing demographic information from the West Virginia Department of Education’s Zoom WV, which also provides attendance rate trends by gender and race, further research can explore whether specific populations are disproportionately affected by floods. The results would reveal if policies on remote learning could be more beneficial for specific demographics. 
  
Additionally, as this research does not contribute to identifying the specific channels through which flooding influences school absences, there is an opportunity for further investigation. For instance, additional research could explore whether students miss classes due to health issues triggered by flooding or face physical challenges in getting to school.

  2. Weaknesses
  
There are a few ways one can improve upon this research. Due to data limitations, I could only find information on attendance rates by school year. Therefore, precipitation and flood incident data are also aggregated on a school-year level. Access to monthly or daily data would enhance the ability to observe more variations and fluctuations in the effects of flooding and discern how various rainfall levels affect attendance rates. Monthly or daily data would also more effectively capture the immediate impact of flood events. With monthly data, one can also consider using month-fixed effects to help improve the model's fit and control for any changing factors within the month for each county. 

This research also does not address the consequences of school closures resulting from flooding on student performance, given that students would have to miss classes during such closures. The West Virginia education website does not inform or specify incidents of school closures. Consequently, it is reasonable to expect that the true impact of flooding on attendance and student performance could be more significant. Our results may be on the conservative side, as it is assumed that the attendance rate data might not capture absences caused by school closures.
