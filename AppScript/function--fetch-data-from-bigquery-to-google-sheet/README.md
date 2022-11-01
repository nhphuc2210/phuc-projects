
# **BigQuery to Google Sheet**

```js
/**
 * Runs a BigQuery query and logs the results in a spreadsheet.
 */
function runQuery() {
  Logger.log("BigQuery To Sheet")

  // Replace this value with the project ID listed in the Google
  // Cloud Platform project.
  const projectId = 'cloud-service-322312';

  const request = {
    // TODO (developer) - Replace query with yours
    query: `select *
from my_schema.cpas_hitlist
where group_cat is not null
limit 10`,
    useLegacySql: false
  };
  let queryResults = BigQuery.Jobs.query(request, projectId);
  const jobId = queryResults.jobReference.jobId;

  // Check on status of the Query Job.
  let sleepTimeMs = 500;
  while (!queryResults.jobComplete) {
    Utilities.sleep(sleepTimeMs);
    sleepTimeMs *= 2;
    queryResults = BigQuery.Jobs.getQueryResults(projectId, jobId);
  }

  // Get all the rows of results.
  let rows = queryResults.rows;
  while (queryResults.pageToken) {
    queryResults = BigQuery.Jobs.getQueryResults(projectId, jobId, {
      pageToken: queryResults.pageToken
    });
    rows = rows.concat(queryResults.rows);
  }

  if (!rows) {
    Logger.log('No rows returned.');
    return;
  }
  // const spreadsheet = SpreadsheetApp.create('BiqQuery Results');
  const spreadsheet = SpreadsheetApp.openById("1qHRqfQx5CkJ7WqXfCyIHRrA-7M-gwNAAuGB8BDuhOGI")
  // const sheet = spreadsheet.getActiveSheet();
  const sheet = spreadsheet.getSheetByName('get_data');

  // Append the headers.
  const headers = queryResults.schema.fields.map(function(field) {
    return field.name;
  });
  sheet.appendRow(headers);

  // Append the results.
  var data = new Array(rows.length);
  for (let i = 0; i < rows.length; i++) {
    const cols = rows[i].f;
    data[i] = new Array(cols.length);
    for (let j = 0; j < cols.length; j++) {
      data[i][j] = cols[j].v;
    }
  }
  sheet.getRange(2, 1, rows.length, headers.length).setValues(data);

  Logger.log('Results spreadsheet created: %s',
      spreadsheet.getUrl());
}

```


