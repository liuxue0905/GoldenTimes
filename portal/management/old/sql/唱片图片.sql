SELECT
records.title AS 唱片标题,
records.number AS 唱片编号,
record_images.type AS 图片类型,
files.path AS 图片路径,
files.mimetype AS 媒体类型
FROM
records
JOIN record_images
ON records.id = record_images.recordId 
LEFT JOIN files
ON record_images.file_id = files.id