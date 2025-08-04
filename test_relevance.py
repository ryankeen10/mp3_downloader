#!/usr/bin/env python3

from CreateSongMenu import CreateSongMenu

def test_relevance_filtering():
    print("🔍 Testing SZA search with relevance filtering...")
    
    menu = CreateSongMenu()
    
    # Test our new relevance filtering
    print("\n1. Testing relevance filtering for 'SZA':")
    
    # Get raw results
    raw_results = menu.sp.search(q="SZA", type="artist", limit=20)
    all_artists = raw_results["artists"]["items"]
    
    print(f"Raw results: {len(all_artists)} artists")
    for i, artist in enumerate(all_artists[:10], 1):
        relevant = menu._is_relevant_match(artist['name'], 'SZA')
        score = menu._calculate_relevance_score(artist, 'SZA')
        print(f"  {i}. {artist['name']} - Relevant: {relevant}, Score: {score:.1f}")
    
    # Filter for relevant results only
    relevant_artists = [a for a in all_artists if menu._is_relevant_match(a['name'], 'SZA')]
    relevant_artists = sorted(relevant_artists, key=lambda x: menu._calculate_relevance_score(x, 'SZA'), reverse=True)
    
    print(f"\nFiltered results: {len(relevant_artists)} relevant artists")
    for i, artist in enumerate(relevant_artists[:10], 1):
        score = menu._calculate_relevance_score(artist, 'SZA')
        print(f"  {i}. {artist['name']} (popularity: {artist.get('popularity', 0)}, score: {score:.1f})")

if __name__ == "__main__":
    test_relevance_filtering()
