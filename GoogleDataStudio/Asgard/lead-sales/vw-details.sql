
create or replace view project.vw_details as (
with sales_data as (
SELECT  P15_bookingsId
        , Email
        , PARSE_DATETIME('%m/%d/%Y %H:%M:%S %p', DateBooked) as DateBooked
        , cast(split(TotalInvoiceNoDiscounts, '.')[offset(0)] as int64) TotalInvoiceNoDiscounts
        , cast(split(TotalRevenues, '.')[offset(0)] as int64) TotalRevenues
FROM `danh-298607.project.CustomBookingFact` 
)

, inquiry_data as (
SELECT  Email
        , PARSE_DATETIME('%m/%d/%Y %H:%M:%S %p', DateOfFirstContact) as DateOfFirstContact
        , LeadSource
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

select a.Email, a.DateBooked, a.TotalInvoiceNoDiscounts, a.TotalRevenues
, DateOfFirstContact, LeadSource, CampaignSource, CampaignMedium, CampaignName, CampaignTerm, CampaignContent
from sales_data a 
left join inquiry_data b on lower(a.email) = lower(b.email)
)

