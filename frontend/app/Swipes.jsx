
import { Ionicons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";
import { useRef } from "react";
import {
  Animated,
  Dimensions,
  Image,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

const { height, width } = Dimensions.get("window");

const DATA = [
  {
    id: "1",
    music: "Nome da Música",
    artist: "Nome do Artista",
    description:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image:
      "https://i.imgur.com/Nc3uQ2W.png", 
    artistImage:
      "https://i.pravatar.cc/100", 
  },
  {
    id: "2",
    music: "Outra Música",
    artist: "Outro Artista",
    description:
      "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    image:
      "https://i.imgur.com/Nc3uQ2W.png",
    artistImage: "https://i.pravatar.cc/101",
  },
];

export default function SwipeMusic() {
  const scrollY = useRef(new Animated.Value(0)).current;

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
            </LinearGradient>
          </View>
        )}
      />
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
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.4,
    shadowRadius: 8,
    elevation: 10,
  },
  musicTitle: {
    fontSize: 20,
    color: "#fff",
    fontWeight: "700",
    textAlign: "center",
    marginBottom: 25,
  },
  artistCard: {
    width: "85%",
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
});
