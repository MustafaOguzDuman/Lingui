import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.youtube.YouTube;
import com.google.api.services.youtube.model.CaptionListResponse;
import com.google.api.services.youtube.model.SearchListResponse;
import com.google.api.services.youtube.model.SearchResult;
//import com.google.api.services.youtube.model.Video;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;

public class VideoRetriever {
    private static final String API_KEY = "AIzaSyB1xKKoNx7V-3sT6VWpOyFp3uFEJaNT8m4";
    private List<String> words;

    public VideoRetriever(List<String> words) {
        this.words = words;
    }

    public List<String> retrieveVideos() throws IOException, GeneralSecurityException {
        NetHttpTransport transport = GoogleNetHttpTransport.newTrustedTransport();
        final JsonFactory JSON_FACTORY = new JacksonFactory();
        //connect to YT API
        YouTube youtube = new YouTube.Builder(transport, JSON_FACTORY, request -> {})
                .setApplicationName("video-retriever")
                .build();

        //Create search query
        String query = String.join(" ", words);
        YouTube.Search.List search = youtube.search().list("id,snippet");
        search.setKey(API_KEY);
        search.setQ(query);
        //search.setQ("surfing");

        //search setting
        //for more: https://developers.google.com/youtube/v3/docs/search/list
        search.setType("video");
        search.setVideoCaption("closedCaption");
        search.setRegionCode("US");
        search.setVideoDuration("short");
        search.setVideoCategoryId("2");
        search.setFields("items(id(videoId),snippet(title,channelId,channelTitle,publishedAt))");
        search.setMaxResults(10L);

        //get results
        SearchListResponse response = search.execute();
        List<SearchResult> results = response.getItems();

        /*List<Video> videos = new ArrayList<>();
        for (SearchResult result : results) {
            Video video = new Video(
                    result.getId().getVideoId(),
                    result.getSnippet().getTitle(),
                    result.getSnippet().getChannelId(),
                    result.getSnippet().getChannelTitle(),
                    result.getSnippet().getPublishedAt()
            );
            videos.add(video);
        }*/
        CaptionListResponse cl = null;
        List<String> videos = new ArrayList<>();
        String id = "";
        for (SearchResult result : results) {
            String video = "";
            video += result.getId().getVideoId();
            video += "=======" ;
            video += result.getSnippet().getTitle();
            //video += result.getSnippet().getChannelId();
            video += "=======" ;
            video += result.getSnippet().getChannelTitle();
            video += "=======" ;
            video += result.getSnippet().getPublishedAt();
            videos.add(video);
            id = result.getId().getVideoId().toString();
            // Define and execute the API request
            
        }
        YouTube.Captions.List request = youtube.captions()
                .list("id", id);
        request.setKey(API_KEY);
        cl = request.execute();
        System.out.println(cl);
        OutputStream output = new FileOutputStream("YOUR_FILE");
        YouTube.Captions.Download red = youtube.captions()
            .download(cl.getItems().get(0).getId());
        red.getMediaHttpDownloader();
        red.executeMediaAndDownloadTo(output);

        return videos;
    }
}
