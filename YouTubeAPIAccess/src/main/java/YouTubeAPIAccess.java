import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.ArrayList;
import java.util.List;

public class YouTubeAPIAccess {
    public static void main(String[] args) throws GeneralSecurityException, IOException {
        List<String> words = new ArrayList<>();
        words.add("beautiful");
        VideoRetriever videoRetriever = new VideoRetriever(words);
        List<String> results = videoRetriever.retrieveVideos();
        for (String s: results ) {
            System.out.println(s);
        }
    }
}
