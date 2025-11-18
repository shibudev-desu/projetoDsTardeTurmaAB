import { Ionicons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";
import { useRef, useState, useEffect } from "react";
import {
  Animated,
  Dimensions,
  Image,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  Modal,
  Share,
} from "react-native";

const { height, width } = Dimensions.get("window");

const DATA = [
  {
    id: "1",
    music: "Nome da Música",
    artist: "Nome do Artista",
    description:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
    lyrics:
      "Letra da música...\nLorem ipsum dolor sit amet...\nMais verso...",
    image: "https://i.imgur.com/Nc3uQ2W.png",
    artistImage: "https://i.pravatar.cc/100",
  },
  {
    id: "2",
    music: "Outra Música",
    artist: "Outro Artista",
    description:
      "Ut enim ad minim veniam, quis nostrud exercitation...",
    lyrics:
      "Outra letra...\nMais versos...",
    image: "https://i.imgur.com/Nc3uQ2W.png",
    artistImage: "https://i.pravatar.cc/101",
  },
];

export default function SwipeMusic() {
  const scrollY = useRef(new Animated.Value(0)).current;
  const progress = useRef(new Animated.Value(0)).current;

  const [showLyrics, setShowLyrics] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [liked, setLiked] = useState(false);

 
  useEffect(() => {
    Animated.loop(
      Animated.timing(progress, {
        toValue: 1,
        duration: 6000,
        useNativeDriver: false,
      })
    ).start();
  }, []);

  const progressWidth = progress.interpolate({
    inputRange: [0, 1],
    outputRange: ["0%", "100%"],
  });

  const shareMusic = async (music) => {
    await Share.share({
      message: `Estou ouvindo: ${music.music} - ${music.artist}`,
    });
  };

  return (
    <View style={styles.container}>
      <Animated.FlatList
        data={DATA}
        keyExtractor={(item) => item.id}
        pagingEnabled
        showsVerticalScrollIndicator={false}
        onScroll={Animated.event(
          [{ nativeEvent: { contentOffset: { y: scrollY } } }],
          { useNativeDriver: true }
        )}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Image source={{ uri: item.image }} style={styles.background} />

            <LinearGradient
              colors={["#8000d5", "#f910a3", "#fddf00"]}
              style={styles.gradient}
            >
              
              <TouchableOpacity style={styles.playButton}>
                <LinearGradient
                  colors={["#fddf00", "#f910a3"]}
                  style={styles.playCircle}
                >
                  <Ionicons name="play" size={50} color="#fff" />
                </LinearGradient>
              </TouchableOpacity>

             
              <TouchableOpacity
                onPress={() => setLiked(!liked)}
                style={styles.likeButton}
              >
                <Ionicons
                  name={liked ? "heart" : "heart-outline"}
                  size={40}
                  color={liked ? "#ff0049" : "#fff"}
                />
              </TouchableOpacity>

              
              <TouchableOpacity
                onPress={() => shareMusic(item)}
                style={styles.shareButton}
              >
                <Ionicons name="share-social" size={35} color="#fff" />
              </TouchableOpacity>

              
              <View style={styles.progressBar}>
                <Animated.View
                  style={[styles.progressFill, { width: progressWidth }]}
                />
              </View>

              <Text style={styles.musicTitle}>{item.music}</Text>

              
              <LinearGradient
                colors={["#ff00cc", "#ffcc00"]}
                style={styles.artistCard}
              >
                <View style={styles.artistRow}>
                  <Image
                    source={{ uri: item.artistImage }}
                    style={styles.artistImage}
                  />

                  <View style={{ flex: 1 }}>
                    <Text style={styles.artistName}>{item.artist}</Text>
                    <Text style={styles.artistDesc}>{item.description}</Text>
                  </View>
                </View>
              </LinearGradient>

              
              <TouchableOpacity
                onPress={() => {
                  setSelectedItem(item);
                  setShowLyrics(true);
                }}
              >
                <Text style={styles.lyricsText}>Ver Letra ↑</Text>
              </TouchableOpacity>
            </LinearGradient>
          </View>
        )}
      />

      
      <Modal visible={showLyrics} animationType="slide" transparent>
        <View style={styles.modalContainer}>
          <View style={styles.modalBox}>
            <Text style={styles.modalTitle}>Letra</Text>

            <Text style={styles.modalLyrics}>
              {selectedItem?.lyrics || "Sem letra disponível."}
            </Text>

            <TouchableOpacity
              onPress={() => setShowLyrics(false)}
              style={styles.modalClose}
            >
              <Text style={{ color: "#fff", fontSize: 18 }}>Fechar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000",
  },
  card: {
    width,
    height,
    alignItems: "center",
    justifyContent: "center",
  },
  background: {
    ...StyleSheet.absoluteFillObject,
  },
  gradient: {
    flex: 1,
    justifyContent: "flex-end",
    alignItems: "center",
    paddingBottom: 60,
  },

  
  playButton: {
    position: "absolute",
    top: height * 0.3,
  },
  playCircle: {
    width: 120,
    height: 120,
    borderRadius: 60,
    justifyContent: "center",
    alignItems: "center",
    elevation: 10,
  },
  likeButton: {
    position: "absolute",
    top: height * 0.35,
    right: 25,
  },
  shareButton: {
    position: "absolute",
    top: height * 0.42,
    right: 25,
  },

  
  progressBar: {
    width: "80%",
    height: 4,
    backgroundColor: "#ffffff40",
    borderRadius: 10,
    marginBottom: 20,
  },
  progressFill: {
    height: 4,
    backgroundColor: "#fff",
    borderRadius: 10,
  },

  musicTitle: {
    fontSize: 22,
    color: "#fff",
    fontWeight: "700",
    textAlign: "center",
    marginBottom: 25,
  },

  
  artistCard: {
    width: "87%",
    borderRadius: 20,
    padding: 12,
  },
  artistRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  artistImage: {
    width: 50,
    height: 50,
    borderRadius: 25,
    marginRight: 12,
  },
  artistName: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 5,
    
  },
  artistDesc: {
    color: "#fff",
    fontSize: 12,
  },

  lyricsText: {
    marginTop: 20,
    fontSize: 14,
    color: "#fff",
    opacity: 0.8,
  },

 
  modalContainer: {
    flex: 1,
    backgroundColor: "#000a",
    justifyContent: "flex-end",
  },
  modalBox: {
    backgroundColor: "#222",
    padding: 20,
    borderTopLeftRadius: 25,
    borderTopRightRadius: 25,
    maxHeight: height * 0.7,
  },
  modalTitle: {
    color: "#fff",
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 10,
  },
  modalLyrics: {
    color: "#ddd",
    fontSize: 16,
    marginBottom: 20,
  },
  modalClose: {
    backgroundColor: "#f910a3",
    padding: 12,
    alignItems: "center",
    borderRadius: 10,
  },
});
