import { View, Text, Image, TouchableOpacity, ScrollView, StyleSheet, Dimensions } from "react-native"
import { Ionicons } from "@expo/vector-icons"
import { LinearGradient } from "expo-linear-gradient"

const { width } = Dimensions.get("window")

const songs = [
  { id: 1, title: "Musica 1" },
  { id: 2, title: "Musica 2" },
  { id: 3, title: "Musica 3" },
  { id: 4, title: "Musica 4" },
  { id: 5, title: "Musica 5" },
  { id: 6, title: "Musica 6" },
  { id: 7, title: "Musica 7" },
]

export default function ArtistProfile() {
  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton}>
          <Ionicons name="chevron-back" size={28} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Perfil Artista</Text>
      </View>

      <View style={styles.artistImageContainer}>
        <Image
          source={{
            uri: "",
          }}
          style={styles.artistImage}
          resizeMode="cover"
        />
        <View style={styles.artistNameOverlay}>
          <Text style={styles.artistName}>GREEN DAY</Text>
        </View>
      </View>

      <View style={styles.actionSection}>
        <View style={styles.followButtonContainer}>
          <TouchableOpacity style={styles.followButton}>
            <Text style={styles.followButtonText}>Seguir</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.menuButton}>
            <Ionicons name="ellipsis-vertical" size={20} color="#fff" />
          </TouchableOpacity>
        </View>
        <View style={styles.playButtons}>
          <TouchableOpacity style={styles.shuffleButton}>
            <Ionicons name="shuffle" size={24} color="#fff" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.playButton}>
            <Ionicons name="play" size={28} color="#000" />
          </TouchableOpacity>
        </View>
      </View>

   
      <LinearGradient colors={["#a020f0", "#d946ef", "#f97316", "#fbbf24"]} style={styles.popularSection}>
        <Text style={styles.popularTitle}>Popular</Text>
        <View style={styles.songsList}>
          {songs.map((song) => (
            <TouchableOpacity key={song.id} style={styles.songItem}>
              <View style={styles.songThumbnail} />
              <Text style={styles.songTitle}>{song.title}</Text>
            </TouchableOpacity>
          ))}
        </View>
        <TouchableOpacity style={styles.discographyButton}>
          <Text style={styles.discographyButtonText}>Ver discografia</Text>
        </TouchableOpacity>
      </LinearGradient>
    </ScrollView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#1a1a1a",
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: "#2a2a2a",
  },
  backButton: {
    width: 40,
    height: 40,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    borderRadius: 20,
  },
  headerTitle: {
    flex: 1,
    fontSize: 18,
    fontWeight: "600",
    color: "#fff",
    marginLeft: 16,
  },
  artistImageContainer: {
    width: width,
    height: 280,
    position: "relative",
  },
  artistImage: {
    width: "100%",
    height: "100%",
  },
  artistNameOverlay: {
    position: "absolute",
    bottom: 16,
    left: 16,
  },
  artistName: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#fff",
    textShadowColor: "rgba(0, 0, 0, 0.75)",
    textShadowOffset: { width: 0, height: 2 },
    textShadowRadius: 4,
  },
  actionSection: {
    backgroundColor: "#a020f0",
    paddingHorizontal: 20,
    paddingVertical: 16,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  followButtonContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },
  followButton: {
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    paddingHorizontal: 24,
    paddingVertical: 10,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "rgba(255, 255, 255, 0.3)",
  },
  followButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
  menuButton: {
    width: 36,
    height: 36,
    justifyContent: "center",
    alignItems: "center",
  },
  playButtons: {
    flexDirection: "row",
    alignItems: "center",
    gap: 16,
  },
  shuffleButton: {
    width: 44,
    height: 44,
    justifyContent: "center",
    alignItems: "center",
  },
  playButton: {
    width: 52,
    height: 52,
    backgroundColor: "#fbbf24",
    borderRadius: 26,
    justifyContent: "center",
    alignItems: "center",
  },
  popularSection: {
    paddingHorizontal: 20,
    paddingTop: 24,
    paddingBottom: 32,
  },
  popularTitle: {
    fontSize: 22,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 16,
  },
  songsList: {
    gap: 12,
  },
  songItem: {
    flexDirection: "row",
    alignItems: "center",
    gap: 16,
    paddingVertical: 8,
  },
  songThumbnail: {
    width: 56,
    height: 56,
    backgroundColor: "rgba(255, 255, 255, 0.3)",
    borderRadius: 4,
  },
  songTitle: {
    fontSize: 16,
    fontWeight: "500",
    color: "#fff",
  },
  discographyButton: {
    backgroundColor: "#fbbf24",
    paddingVertical: 14,
    borderRadius: 25,
    alignItems: "center",
    marginTop: 24,
  },
  discographyButtonText: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#000",
  },
})
