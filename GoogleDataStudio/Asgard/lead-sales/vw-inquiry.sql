
create or replace view project.Fact_Custom_Inquiry as (

with raw_data as (
SELECT Email, 
      date(PARSE_DATETIME('%m/%d/%Y %H:%M:%S %p', DateOfFirstContact)) as DateOfFirstContact, 
      LeadSource
      , CASE WHEN LeadSource LIKE '%utm_source%' 
                  THEN project.decode_url(split(split(LeadSource, 'utm_source=')[safe_offset(1)], '&')[safe_offset(0)])
            ELSE CampaignSource END AS CampaignSource
      , CASE WHEN LeadSource LIKE '%utm_medium%' 
                  THEN project.decode_url(split(split(LeadSource, 'utm_medium=')[safe_offset(1)], '&')[safe_offset(0)])
            ELSE CampaignMedium END AS CampaignMedium
      , CASE WHEN LeadSource LIKE '%utm_campaign%' 
                  THEN project.decode_url(split(split(LeadSource, 'utm_campaign=')[safe_offset(1)], '&')[safe_offset(0)])
            ELSE CampaignName END AS CampaignName
      , CASE WHEN LeadSource LIKE '%utm_term%' 
            THEN project.decode_url(split(split(LeadSource, 'utm_term=')[safe_offset(1)], '&')[safe_offset(0)])
      ELSE CampaignTerm END AS CampaignTerm
      , CASE WHEN LeadSource LIKE '%utm_content%' 
            THEN project.decode_url(split(split(LeadSource, 'utm_content=')[safe_offset(1)], '&')[safe_offset(0)])
      ELSE CampaignContent END AS CampaignContent

FROM `danh-298607.project.CustomInquiryFact` 
)


select Email, 
       min(DateOfFirstContact) over(partition_email) FirstDateContacted, 
       coalesce(first_value(replace(`danh-298607.project.proper`(lower(LeadSource)), '  ', ' ') ignore nulls) over(partition_email), 'Organic') LeadSource,
       coalesce(first_value(replace(`danh-298607.project.proper`(lower(CampaignSource)), '  ', ' ') ignore nulls) over(partition_email), 'Organic') CampaignSource,
       coalesce(first_value(replace(`danh-298607.project.proper`(lower(CampaignMedium)), '  ', ' ') ignore nulls) over(partition_email), 'Organic') CampaignMedium,
       coalesce(first_value(replace(`danh-298607.project.proper`(lower(CampaignName)), '  ', ' ') ignore nulls) over(partition_email), 'Organic') CampaignName,
       coalesce(first_value(replace(`danh-298607.project.proper`(lower(CampaignTerm)), '  ', ' ') ignore nulls) over(partition_email), 'Organic') CampaignTerm,
       coalesce(first_value(replace(`danh-298607.project.proper`(lower(CampaignContent)), '  ', ' ') ignore nulls) over(partition_email), 'Organic') CampaignContent
from raw_data
where Email is not null
window partition_email as (partition by Email order by DateOfFirstContact)

)

