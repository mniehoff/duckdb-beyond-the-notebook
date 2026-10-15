FROM sniff_csv('data/csv/events.csv');

SELECT unnest(Columns)
FROM sniff_csv('data/csv/events.csv');

-- Read the file, storing rejected rows
SELECT * FROM read_csv(
    'data/csv/faulty_folks.csv',
    header = true,
    columns = {'Name': 'VARCHAR', 'Age': 'INTEGER'},
    store_rejects = true -- Store info about errors
);

-- Now, let's see what was rejected
FROM reject_errors;

-- And details about the scan itself
FROM reject_scans;

FROM read_csv('data/csv/inventory.csv',
    strict_mode = false,   -- Forgive formatting quirks
    null_padding = true   -- Fill missing columns with NULLs
);

SELECT *
FROM read_csv(
    ['data/csv/report_jan.csv', 'data/csv/report_feb.csv'], -- List of files (or glob)
    union_by_name = true -- The magic!
);
