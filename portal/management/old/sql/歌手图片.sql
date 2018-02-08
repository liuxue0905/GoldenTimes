SELECT
artists.`name` AS 歌手名称,
artists.type AS 歌手类型,
artist_images.type AS 图片类型,
files.path AS 图片路径,
files.mimetype AS 媒体类型
FROM
artists
JOIN artist_images
ON artists.id = artist_images.artistId 
LEFT JOIN files
ON artist_images.file_id = files.id