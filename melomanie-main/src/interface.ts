export interface RecommendationParams {
    seed_artists: string;
    seed_genres: string;
    seed_tracks: string;
    target_danceability: number;
    target_speechiness: number;
    target_valence: number;
    target_energy: number;
    limit?: number;
}